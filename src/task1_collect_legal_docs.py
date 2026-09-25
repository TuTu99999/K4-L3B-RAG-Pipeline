"""
Task 1 — Thu thập tài liệu chính sách/quy định.

Hướng dẫn:
    1. Chọn chủ đề của nhóm.
    2. Tìm tối thiểu 3 tài liệu PDF/DOCX từ nguồn công khai.
    3. Lưu file gốc vào data/landing/legal/.
    4. Đặt tên không dấu và thể hiện đúng nội dung.

Ví dụ tài liệu: học phí, học bổng, ký túc xá, quy trình đăng ký.
Nếu website chặn crawler, hãy chọn nguồn công khai khác; không vượt WAF.
"""

from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "legal"
LEGAL_SOURCES: dict[str, str] = {}


def setup_directory() -> None:
    """Tạo thư mục lưu tài liệu gốc."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Ready: {DATA_DIR}")


def download_documents() -> None:
    """Tải ít nhất 3 PDF/DOCX từ nguồn công khai."""
    import requests

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for filename, url in LEGAL_SOURCES.items():
        output = DATA_DIR / filename
        if output.exists() and output.stat().st_size > 1024:
            print(f"Already exists: {output}")
            continue

        response = requests.get(url, timeout=30)
        response.raise_for_status()
        output.write_bytes(response.content)
        print(f"Downloaded: {output}")

    documents = [
        path
        for path in DATA_DIR.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".pdf", ".doc", ".docx"}
        and path.stat().st_size > 1024
    ]
    if len(documents) < 3:
        raise RuntimeError(
            "Need at least 3 non-empty PDF/DOC/DOCX files in "
            f"{DATA_DIR}. Add files manually or configure LEGAL_SOURCES."
        )

    print(f"Ready: {len(documents)} legal documents")


if __name__ == "__main__":
    setup_directory()
    download_documents()
