"""Claude 호출 래퍼 (공식 anthropic SDK).

- 모든 LLM 호출은 여기를 거친다 → 호출 수/토큰을 한 곳에서 집계 (eval의 비용 지표용).
- 집계는 스레드별로 분리된다 → eval을 병렬로 돌려도 실행 단위 비용이 섞이지 않는다.
- Claude Haiku 5.5는 temperature 등 sampling 파라미터를 지원하지 않는다(400).
  결과가 완전히 결정적이지 않으므로 평가는 반복 실행 평균으로 본다.
- thinking이 기본으로 켜져 있어 응답 앞에 thinking 블록이 올 수 있다 → text 블록만 모은다.
"""

import threading
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

# $ / 1M tokens (input, output) — 비용 추정용
PRICES = {
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00),
}

_client = anthropic.Anthropic()

T = TypeVar("T", bound=BaseModel)


class LLMRefusalError(RuntimeError):
    pass


@dataclass
class UsageStats:
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cost_usd: float = 0.0
    calls_by_tag: dict[str, int] = field(default_factory=dict)

    def record(self, model: str, tag: str, usage) -> None:
        self.calls += 1
        self.input_tokens += usage.input_tokens
        self.output_tokens += usage.output_tokens
        in_price, out_price = PRICES.get(model, (0.0, 0.0))
        self.cost_usd += (usage.input_tokens * in_price + usage.output_tokens * out_price) / 1_000_000
        self.calls_by_tag[tag] = self.calls_by_tag.get(tag, 0) + 1

    def snapshot(self) -> dict:
        return {
            "calls": self.calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "cost_usd": round(self.cost_usd, 6),
            "calls_by_tag": dict(self.calls_by_tag),
        }


_local = threading.local()


def _stats() -> UsageStats:
    if not hasattr(_local, "stats"):
        _local.stats = UsageStats()
    return _local.stats


def reset_usage() -> None:
    """현재 스레드의 집계를 초기화한다."""
    _local.stats = UsageStats()


def get_usage() -> dict:
    """현재 스레드의 집계 스냅샷."""
    return _stats().snapshot()


def _check_refusal(response, tag: str) -> None:
    if response.stop_reason == "refusal":
        raise LLMRefusalError(f"[{tag}] request refused: {response.stop_details}")


def complete(
    system: str,
    user: str,
    *,
    effort: str = GENERATION_EFFORT,
    tag: str = "complete",
    model: str = MODEL_NAME,
) -> str:
    """자유 텍스트 응답."""
    response = _client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_config={"effort": effort},
    )
    _stats().record(model, tag, response.usage)
    _check_refusal(response, tag)
    return "".join(block.text for block in response.content if block.type == "text").strip()


def structured(
    system: str,
    user: str,
    schema: type[T],
    *,
    effort: str = GRADER_EFFORT,
    tag: str = "structured",
    model: str = MODEL_NAME,
) -> T:
    """Pydantic 스키마로 검증된 구조화 응답 (structured outputs)."""
    response = _client.messages.parse(
        model=model,
        max_tokens=MAX_TOKENS,
        system=system,
        messages=[{"role": "user", "content": user}],
        output_format=schema,
        output_config={"effort": effort},
    )
    _stats().record(model, tag, response.usage)
    _check_refusal(response, tag)
    return response.parsed_output
