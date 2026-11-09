"""Baseline RAG: retrieve → generate (단일 호출)."""

from generation import generate
from retriever import retrieve


def answer_question(
    question: str,
    strategy: str = "markdown",
    k: int = 4,
) -> dict:
    docs = retrieve(query=question, strategy=strategy, k=k)
    answer = generate(question, docs, tag="baseline_generate")

    sources = [
        {
            "source": doc.metadata.get("source"),
            "filename": doc.metadata.get("filename"),
            "chunk_id": doc.metadata.get("chunk_id"),
            "strategy": doc.metadata.get("chunk_strategy"),
        }
        for doc in docs
    ]
    
    return {
        "question": question,
        "strategy": strategy,
        "answer": answer,
        "sources": sources,
    }
    
def print_qa_result(result: dict):
    print("=" * 100)
    print(f"Question: {result['question']}")
    print(f"Strategy: {result['strategy']}")
    print("-" * 100)
    print(result["answer"])
    print("-" * 100)
    print("Sources:")
    for source in result["sources"]:
        print(
            f"- {source['filename']} | "
            f"{source['chunk_id']} | "
            f"{source['strategy']}"
        )
        
if __name__ == "__main__":
    result = answer_question(
        question="외부 API 변경으로 장애가 발생한 사례를 원인과 해결 중심으로 정리해줘",
        strategy="markdown",
        k=4,
    )
    
    print_qa_result(result)