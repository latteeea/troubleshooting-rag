from functools import lru_cache

from langchain_core.documents import Document

from config import CARD_INDEX_DIR, MARKDOWN_INDEX_DIR, RECURSIVE_INDEX_DIR
from vectorstore import load_faiss_vectorstore

INDEX_DIRS = {
    "recursive": RECURSIVE_INDEX_DIR,
    "markdown": MARKDOWN_INDEX_DIR,
    "card": CARD_INDEX_DIR,
}


@lru_cache(maxsize=None)
def _load_vectorstore(strategy: str):
    # Day3-3: 검색 호출마다 인덱스를 디스크에서 다시 읽던 것을 전략별 1회 로드로 변경
    if strategy not in INDEX_DIRS:
        raise ValueError(f"strategy must be one of {list(INDEX_DIRS)}, got {strategy!r}")
    return load_faiss_vectorstore(INDEX_DIRS[strategy])


def get_retriever(strategy: str = "recursive", k: int = 4):
    return _load_vectorstore(strategy).as_retriever(search_kwargs={"k": k})
    
def retrieve(query: str, strategy: str = "recursive", k: int = 4):
    docs = get_retriever(strategy=strategy, k=k).invoke(query)
    if strategy == "card":
        # Day3-4: 카드로 찾고, 생성에는 카드 + 원문 구간을 함께 넘긴다 (근거는 항상 원문)
        docs = [
            Document(
                page_content=f"{d.page_content}\n\n[원문]\n{d.metadata['raw_text']}",
                metadata=d.metadata,
            )
            for d in docs
        ]
    return docs

def print_results(query: str, strategy: str = "recursive", k: int = 4):
    docs = retrieve(query = query, strategy=strategy, k=k)
    
    print(f"\nQuery: {query}")
    print(f"Strategy: {strategy}")
    print(f"Result count: {len(docs)}")
    
    for i, doc in enumerate(docs, start=1):
        print("=" * 80)
        print(f"[{i}] source={doc.metadata.get('source')}")
        print(f"filename={doc.metadata.get('filename')}")
        print(f"chunk_id={doc.metadata.get('chunk_id')}")
        print(doc.page_content[:1000])
        
if __name__ == "__main__":
    test_query = "외부 API 변경으로 장애가 발생한 사례"
    
    print_results(test_query, strategy="recursive", k=3)
    print_results(test_query, strategy="markdown",k=3)