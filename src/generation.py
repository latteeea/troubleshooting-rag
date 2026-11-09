"""답변 생성 (baseline / agentic 공용).

Day3-1: 두 시스템이 같은 프롬프트·같은 입력 형식으로 생성하도록 통일했다.
이전에는 baseline만 "중간 단계는 추측해서 채우고 [추측] 표시"를 허용해서,
두 시스템의 점수 차이가 Self-RAG 루프 때문인지 프롬프트 때문인지 구분할 수 없었다.
기준은 Self-RAG의 hallucination grader가 전제하는 "context 근거만 사용"으로 맞췄다.
"""

from langchain_core.documents import Document

from llm import complete

GENERATION_PROMPT = """너는 사용자의 기술 트러블슈팅 기록을 기반으로 답변하는 RAG assistant다.

규칙:
- 제공된 context만 근거로 답한다. 문서에 없는 내용은 추측하지 않는다.
- 인과 관계 질문이면 A→B→C→D 형태로 시간·원인 순서를 복원한다.
- 답변 구조: 문제 상황 / 조사·원인 / 해결 / 인사이트
- 마지막에 참고 문서 source를 반드시 포함한다."""


def format_docs(docs: list[Document]) -> str:
    formatted = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        chunk_id = doc.metadata.get("chunk_id", "unknown")
        formatted.append(
            f"[문서 {i}]\n"
            f"source: {source}\n"
            f"chunk_id: {chunk_id}\n"
            f"content:\n{doc.page_content}"
        )
    return "\n\n".join(formatted)


def generate(question: str, docs: list[Document], *, tag: str, feedback: str = "") -> str:
    user = f"질문: {question}\n\n검색된 context:\n{format_docs(docs)}"
    if feedback:
        # Day3-2: 재생성 시 직전 답변의 근거 없는 주장을 알려준다 (없으면 같은 입력 → 같은 답이 반복됨)
        user += (
            "\n\n이전 답변에서 context에 근거가 없다고 판정된 내용:\n"
            f"{feedback}\n\n"
            "위 내용을 빼거나 context에 있는 사실로 고쳐서 다시 답하라."
        )
    return complete(GENERATION_PROMPT, user, tag=tag)
