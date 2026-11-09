from typing import Annotated

from langchain_core.documents import Document
from typing_extensions import TypedDict


class GraphState(TypedDict):
    question: Annotated[str, "현재 검색에 사용하는 질문 (rewrite 후 갱신될 수 있음)"]
    original_question: Annotated[str, "사용자가 처음 입력한 질문"]
    generation: Annotated[str, "LLM이 생성한 답변"]
    documents: Annotated[list[Document], "검색·필터링된 문서 목록"]
    strategy: Annotated[str, "청킹 전략 (recursive | markdown)"]
    rewrite_count: Annotated[int, "query rewrite 시도 횟수"]
    generation_attempts: Annotated[int, "답변 생성·재생성 시도 횟수"]
    hallucination_feedback: Annotated[str, "직전 생성에서 근거 없다고 판정된 주장 (재생성 프롬프트에 전달)"]
    grounded: Annotated[bool, "직전 생성이 문서에 근거한다고 판정됐는가"]
    answers_question: Annotated[bool, "직전 생성이 질문에 답한다고 판정됐는가"]
