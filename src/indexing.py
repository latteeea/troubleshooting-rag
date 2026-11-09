from loader import load_md_documents
from splitter import split_recursive, split_md_header

from vectorstore import (
    build_faiss_vectorstore,
    save_faiss_vectorstore,
    reset_faiss_index,
)

import json
import sys

from langchain_core.documents import Document

from config import CARD_INDEX_DIR, CARDS_DIR, DATA_DIR, MARKDOWN_INDEX_DIR, RECURSIVE_INDEX_DIR

def build_recursive_index():
    docs = load_md_documents(str(DATA_DIR))
    
    chunks = split_recursive(docs)
    
    print(f"[Recursive] chunk count: {len(chunks)}")
    
    vectorstore = build_faiss_vectorstore(chunks)
    
    reset_faiss_index(RECURSIVE_INDEX_DIR)
    
    save_faiss_vectorstore(
        vectorstore,
        RECURSIVE_INDEX_DIR,
    )
    
    print(f"Saved recursive index -> {RECURSIVE_INDEX_DIR}")
    
def build_markdown_index():
    docs = load_md_documents(str(DATA_DIR))
    
    chunks = split_md_header(docs)
    
    print(f"[Markdown Header] chunk count: {len(chunks)}")
    
    vectorstore = build_faiss_vectorstore(chunks)
    
    reset_faiss_index(MARKDOWN_INDEX_DIR)
    
    save_faiss_vectorstore(
        vectorstore,
        MARKDOWN_INDEX_DIR,
    )
    
    print(f"Saved markdown index -> {MARKDOWN_INDEX_DIR}")
    
def load_card_documents() -> list[Document]:
    """cards/**/*.json → 카드 1장 = Document 1개. 임베딩은 카드 텍스트, 원문 구간은 metadata로 보관."""
    from cards import card_to_text

    docs = []
    for path in sorted(CARDS_DIR.rglob("*.json")):
        for card in json.loads(path.read_text(encoding="utf-8")):
            docs.append(
                Document(
                    page_content=card_to_text(card),
                    metadata={
                        "source": card["source"],
                        "filename": card["filename"],
                        "chunk_id": card["card_id"],
                        "chunk_strategy": "card",
                        "kind": card["kind"],
                        "raw_text": card["raw_text"],
                    },
                )
            )
    return docs


def build_card_index():
    docs = load_card_documents()
    print(f"[Card] card count: {len(docs)}")
    vectorstore = build_faiss_vectorstore(docs)
    reset_faiss_index(CARD_INDEX_DIR)
    save_faiss_vectorstore(vectorstore, CARD_INDEX_DIR)
    print(f"Saved card index -> {CARD_INDEX_DIR}")


if __name__ == "__main__":
    targets = sys.argv[1:] or ["recursive", "markdown", "card"]
    if "recursive" in targets:
        build_recursive_index()
    if "markdown" in targets:
        build_markdown_index()
    if "card" in targets:
        build_card_index()
