"""Claude 호출 래퍼 (공식 anthropic SDK).

- 모든 LLM 호출은 여기를 거친다 → 호출 수/토큰을 한 곳에서 집계 (eval의 비용 지표용).
- Claude Haiku 5.5는 temperature 등 sampling 파라미터를 지원하지 않는다(400).
  결과가 완전히 결정적이지 않으므로 평가는 반복 실행 평균으로 본다.
- thinking이 기본으로 켜져 있어 응답 앞에 thinking 블록이 올 수 있다 → text 블록만 모은다.
"""

from dataclasses import dataclass, field
from typing import TypeVar

import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

MODEL_NAME = "claude-haiku-5-5"
MAX_TOKENS = 16000

# 생성은 기본(medium), grader/rewriter 같은 단순 판정은 low
GENERATION_EFFORT = "medium"
GRADER_EFFORT = "low"

_client = anthropic.Anthropic()

T = TypeVar("T", bound=BaseModel)


class LLMRefusalError(RuntimeError):
    pass


@dataclass
class UsageStats:
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    calls_by_tag: dict[str, int] = field(default_factory=dict)

    def record(self, tag: str, usage) -> None:
        self.calls += 1
        self.input_tokens += usage.input_tokens
        self.output_tokens += usage.output_tokens
        self.calls_by_tag[tag] = self.calls_by_tag.get(tag, 0) + 1

    def snapshot(self) -> dict:
        return {
            "calls": self.calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "calls_by_tag": dict(self.calls_by_tag),
        }


usage_stats = UsageStats()


def reset_usage() -> None:
    global usage_stats
    usage_stats = UsageStats()


def get_usage() -> dict:
    return usage_stats.snapshot()


def _check_refusal(response, tag: str) -> None:
    if response.stop_reason == "refusal":
        raise LLMRefusalError(f"[{tag}] request refused: {response.stop_details}")


def complete(system: str, user: str, *, effort: str = GENERATION_EFFORT, tag: str = "complete") -> str:
    """자유 텍스트 응답."""
    response = _client.messages.create(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_config={"effort": effort},
    )
    usage_stats.record(tag, response.usage)
    _check_refusal(response, tag)
    return "".join(block.text for block in response.content if block.type == "text").strip()


def structured(system: str, user: str, schema: type[T], *, effort: str = GRADER_EFFORT, tag: str = "structured") -> T:
    """Pydantic 스키마로 검증된 구조화 응답 (structured outputs)."""
    response = _client.messages.parse(
        model=MODEL_NAME,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_format=schema,
        output_config={"effort": effort},
    )
    usage_stats.record(tag, response.usage)
    _check_refusal(response, tag)
    return response.parsed_output
