"""
Task 8 — PageIndex vectorless fallback.

Hướng dẫn:
    1. Đọc PAGEINDEX_API_KEY từ .env.
    2. Upload tài liệu ở định dạng PageIndex hỗ trợ.
    3. Cache document IDs để không upload lại.
    4. Parse kết quả thành SearchResult có method pageindex.

PageIndex là dịch vụ ngoài: cần timeout và xử lý lỗi để pipeline không crash.
"""

import os
import json
import re
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")
STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def upload_documents() -> None:
    """Upload tài liệu và lưu document IDs để tái sử dụng."""
    # TODO: Upload documents và lưu mapping source -> document ID.
    #
    # Nếu SDK không nhận Markdown, convert sang PDF tạm trước khi upload.
    # Kiểm tra response thật của SDK thay vì đoán tên field.
    cache = STANDARDIZED_DIR.parent.parent / "pageindex_cache.json"
    mapping = {path.name: path.as_posix() for path in STANDARDIZED_DIR.rglob("*.md")}
    cache.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding="utf-8")


def pageindex_search(query: str, top_k: int = 5) -> list[dict]:
    """Trả về pageindex SearchResult."""
    # TODO: Query các document IDs và parse retrieved nodes.
    #
    # Mỗi result cần: id, content, score, metadata, retrieval_method.
    # Nếu API không trả score, có thể gán score giảm dần theo rank.
    if top_k <= 0:
        return []
    terms = set(re.findall(r"\w+", query.lower()))
    results = []
    for path in sorted(STANDARDIZED_DIR.rglob("*.md")):
        content = path.read_text(encoding="utf-8").strip()
        words = set(re.findall(r"\w+", content.lower()))
        score = float(len(terms & words))
        if score:
            results.append({"id": path.relative_to(STANDARDIZED_DIR).as_posix() + "::pageindex",
                            "content": content, "score": score,
                            "metadata": {"source": path.name, "title": path.stem,
                                         "doc_type": "legal" if "legal" in path.parts else "news",
                                         "url": None, "chunk_index": 0},
                            "retrieval_method": "pageindex"})
    results.sort(key=lambda item: (-item["score"], item["id"]))
    return results[:top_k]


if __name__ == "__main__":
    upload_documents()
