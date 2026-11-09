from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

# data/public: 레포에 공개되는 문서, data/private: 로컬 전용 (gitignore)
# loader가 rglob으로 하위 폴더까지 읽으므로 둘 다 인덱싱된다.
DATA_DIR = ROOT_DIR / "data"

CACHE_ROOT = ROOT_DIR / "cache"
RECURSIVE_INDEX_DIR = str(CACHE_ROOT / "faiss_recursive")
MARKDOWN_INDEX_DIR = str(CACHE_ROOT / "faiss_markdown")

# Day3-4: 기록 → 카드 정리 결과 (cards/private는 gitignore)
CARDS_DIR = ROOT_DIR / "cards"
CARD_INDEX_DIR = str(CACHE_ROOT / "faiss_card")
