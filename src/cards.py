"""막 적은 기록 → 카드(정형화된 단위) 스키마.

설계 원칙
- 카드 1장 = 독립적으로 이해 가능한 단위 하나 (트러블슈팅 사례 1건, 설계 결정 1건, 회고 1건).
  한 파일에 사례가 여러 개면 카드도 여러 장 (예: nginx_deploy.md → 4장).
- 카드는 "검색용 색인"이다. 생성에는 카드 + 원문 구간(source_lines)을 함께 넘긴다.
  → 카드 정리 LLM의 오류가 답변 근거로 섞이지 않게, 근거는 항상 원문.
- source_lines는 원문 줄 번호 범위. LLM에 줄 번호를 붙인 원문을 주고 범위를 받는다.
  → 코드로 원문을 정확히 잘라낼 수 있고, 범위가 유효한지 검증할 수 있다.
- kind로 카드 종류를 나눈다. 연구 노트(kind="research")는 이후 확장으로 남겨둔다.
"""

import json
import sys
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, Field

import llm
from config import CARDS_DIR, DATA_DIR, ROOT_DIR


class Attempt(BaseModel):
    """조사 중 세운 가설과 그 결과. 사고 과정(Engineering Narrative)의 재료."""

    hypothesis: str = Field(description="의심했던 원인 또는 시도한 방법")
    result: Literal["confirmed", "rejected", "partial", "unknown"] = Field(
        description="기록상 그 가설/시도가 맞았는지"
    )
    evidence: str = Field(default="", description="그렇게 판단한 근거 (기록에 있는 확인 방법·관찰)")


class SourceSpan(BaseModel):
    start_line: int = Field(description="원문 시작 줄 번호 (1부터, 포함)")
    end_line: int = Field(description="원문 끝 줄 번호 (포함)")


class CardBase(BaseModel):
    title: str = Field(description="사례를 한 줄로 요약한 제목 (검색에 쓰이므로 증상·대상 기술을 포함)")
    tech_stack: list[str] = Field(default_factory=list, description="관련 기술·도구 (예: Nginx, Expo, PostgreSQL)")
    keywords: list[str] = Field(
        default_factory=list,
        description="기록에 실제로 나오는 고유 용어·에러 메시지·설정 키 (기록에 없는 용어는 넣지 않는다)",
    )
    source_lines: list[SourceSpan] = Field(description="이 카드의 근거가 되는 원문 구간들")


class TroubleshootingCard(CardBase):
    kind: Literal["troubleshooting"] = "troubleshooting"
    symptom: str = Field(description="겉으로 드러난 증상 (에러 메시지, 관찰된 현상)")
    context: str = Field(default="", description="발생 상황·환경 (언제, 무엇을 하다가, 어떤 환경에서)")
    attempts: list[Attempt] = Field(default_factory=list, description="조사 과정에서 세운 가설과 시도, 시간 순서대로")
    root_cause: str = Field(default="", description="최종 원인. 기록에 명확하지 않으면 빈 문자열")
    resolution: str = Field(default="", description="해결 방법. 미해결이면 빈 문자열")
    insights: list[str] = Field(default_factory=list, description="기록에 적힌 교훈·인사이트")


class DecisionCard(CardBase):
    kind: Literal["decision"] = "decision"
    problem: str = Field(description="결정이 필요했던 문제 상황")
    options: list[str] = Field(default_factory=list, description="검토한 선택지")
    decision: str = Field(description="최종 선택")
    rationale: str = Field(description="선택 이유 / 트레이드오프")
    outcome: str = Field(default="", description="결정 이후 결과 (기록에 있으면)")


class NoteCard(CardBase):
    """회고, 블로그 초안, 평가 메모 등 사례·결정 형태가 아닌 기록."""

    kind: Literal["note"] = "note"
    summary: str = Field(description="핵심 내용 요약 (3~5문장)")
    claims: list[str] = Field(default_factory=list, description="기록에 담긴 주요 주장·사실·수치")


Card = Annotated[TroubleshootingCard | DecisionCard | NoteCard, Field(discriminator="kind")]


class DocumentCards(BaseModel):
    """원문 파일 하나에서 추출한 카드 묶음."""

    cards: list[Card] = Field(description="파일 안의 독립적인 단위마다 카드 1장")


# ---------------------------------------------------------------- 추출

EXTRACT_MODEL = "claude-sonnet-5-5"
EXTRACT_EFFORT = "medium"

EXTRACT_PROMPT = """너는 개발자가 막 적어둔 기술 기록을 검색용 카드로 정리한다.
원문의 각 줄 앞에는 줄 번호가 붙어 있다.

카드 나누기
- 독립적으로 이해 가능한 단위마다 카드 1장. 한 파일에 사례가 여러 개면 나눈다.
- 같은 사례의 문제·원인·해결이 원문에서 떨어져 있어도 한 카드로 묶는다.
- kind 선택:
  - troubleshooting: 문제(에러·장애·버그)가 있고 그 원인이나 해결을 다룬 기록
  - decision: 여러 선택지 중 무엇을 왜 골랐는지(설계·기술 선택)를 다룬 기록
  - note: 위 둘에 해당하지 않는 회고, 블로그 초안, 평가 메모, 측정 결과 정리 등
- 문서에 사례가 하나도 없으면 note 카드로 정리한다.

내용 규칙
- 원문에 있는 내용만 쓴다. 원문에 없으면 빈 값으로 둔다. 추측하거나 일반 지식으로 보충하지 않는다.
- keywords에는 원문에 실제로 나오는 표현만 그대로 넣는다 (에러 메시지, 설정 키, 도구명 등).
- attempts에는 원문에 드러난 의심·시도·확인 과정을 시간 순서대로 넣는다.
- 수치(오류율, 개수, 시간 등)는 원문 그대로 옮긴다.
- 한국어로 쓴다.

source_lines
- 카드 내용의 근거가 되는 원문 구간을 줄 번호로 지정한다. 여러 구간이어도 된다.
- 같은 사례의 문제·원인·해결 구간을 빠짐없이 포함한다.
- 긴 로그·환경변수 덤프는 핵심 에러 줄만 포함하고 나머지는 제외한다."""


def number_lines(text: str) -> tuple[str, list[str]]:
    lines = text.splitlines()
    width = len(str(len(lines)))
    return "\n".join(f"{i:>{width}}| {line}" for i, line in enumerate(lines, start=1)), lines


def extract_document(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    numbered, lines = number_lines(text)
    user = f"파일명: {path.name}\n\n원문:\n{numbered}"
    result = llm.structured(
        EXTRACT_PROMPT, user, DocumentCards,
        effort=EXTRACT_EFFORT, tag="card_extract", model=EXTRACT_MODEL,
    )

    cards = []
    for i, card in enumerate(result.cards):
        spans, problems = [], []
        for span in card.source_lines:
            start, end = max(1, span.start_line), min(len(lines), span.end_line)
            if start > end:
                problems.append(f"invalid span {span.start_line}-{span.end_line}")
                continue
            spans.append((start, end))
        data = card.model_dump()
        data["card_id"] = f"{path.stem}-card-{i}"
        data["filename"] = path.name
        data["source"] = path.resolve().relative_to(ROOT_DIR).as_posix()
        data["raw_text"] = "\n\n".join("\n".join(lines[s - 1:e]) for s, e in sorted(spans))
        data["span_problems"] = problems
        cards.append(data)
    return cards


def card_to_text(card: dict) -> str:
    """임베딩·생성에 쓰는 카드의 텍스트 표현."""
    parts = [f"[{card['kind']}] {card['title']}"]
    if card.get("tech_stack"):
        parts.append("기술: " + ", ".join(card["tech_stack"]))
    labels = {
        "context": "상황", "symptom": "증상", "root_cause": "원인", "resolution": "해결",
        "problem": "문제", "decision": "결정", "rationale": "이유", "outcome": "결과",
        "summary": "요약",
    }
    for key, label in labels.items():
        if card.get(key):
            parts.append(f"{label}: {card[key]}")
    if card.get("options"):
        parts.append("선택지: " + " / ".join(card["options"]))
    for a in card.get("attempts", []):
        parts.append(f"시도({a['result']}): {a['hypothesis']}" + (f" — {a['evidence']}" if a.get("evidence") else ""))
    for key, label in (("insights", "인사이트"), ("claims", "주요 내용")):
        for item in card.get(key, []):
            parts.append(f"{label}: {item}")
    if card.get("keywords"):
        parts.append("키워드: " + ", ".join(card["keywords"]))
    return "\n".join(parts)


def extract_all(only: list[str] | None = None) -> None:
    """data/{public,private}/*.md → cards/{public,private}/<stem>.json"""
    for path in sorted(DATA_DIR.rglob("*.md")):
        if only and path.stem not in only:
            continue
        out = CARDS_DIR / path.parent.name / f"{path.stem}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        llm.reset_usage()
        cards = extract_document(path)
        out.write_text(json.dumps(cards, ensure_ascii=False, indent=2), encoding="utf-8")
        usage = llm.get_usage()
        kinds = [c["kind"] for c in cards]
        problems = sum(len(c["span_problems"]) for c in cards)
        print(f"{path.name}: {len(cards)} cards {kinds} span_problems={problems} cost=${usage['cost_usd']:.4f}", flush=True)


if __name__ == "__main__":
    extract_all(sys.argv[1:] or None)
