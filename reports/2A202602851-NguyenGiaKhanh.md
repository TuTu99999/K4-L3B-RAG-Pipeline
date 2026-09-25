# Individual contribution report

## Thông tin

- Họ và tên: Nguyễn Gia Khánh
- Mã học viên: 2A202602851
- Nhóm: 4aesieunhan
- Repository/branch: https://github.com/TuTu99999/K4-L3B-RAG-Pipeline/tree/nguyengiakhanh

## Phần việc đã thực hiện

| Module/deliverable | Việc tôi trực tiếp làm | File | Trạng thái |
|---|---|---|---|
| Task 4 — Chunking, embedding, indexing | Đọc Markdown chuẩn hóa; recursive chunking; giữ ID và metadata ổn định; embedding local/fallback offline; ChromaDB cosine và upsert. | `src/task4_chunking_indexing.py` | Done |
| Task 5 — Dense search | Dùng chung `embed_texts()`; query ChromaDB; đổi cosine distance thành similarity; trả `SearchResult` đã sort. | `src/task5_semantic_search.py` | Done |
| Task 6 — BM25 search | Xây BM25 trên cùng corpus chunks; trả score, metadata và `retrieval_method="bm25"`. | `src/task6_lexical_search.py` | Done |
| Task 7 — RRF reranking | Fuse ranked lists bằng RRF; deduplicate theo ID; đánh dấu kết quả `hybrid`. | `src/task7_reranking.py` | Done |

## Quyết định kỹ thuật quan trọng

1. **ID ổn định:** dùng dạng `document_id::chunk-index` và Chroma `upsert`, giúp chạy lại pipeline không tạo bản ghi trùng. Trade-off là thay đổi nội dung có thể làm thay đổi ID của các chunk phía sau.

2. **RRF cho dense + BM25:** chỉ kết hợp thứ hạng vì cosine và BM25 có thang điểm khác nhau. Cách này tránh phải hiệu chỉnh score giữa hai retriever, nhưng không tận dụng độ lớn tuyệt đối của score.

## Kiểm thử và kết quả

- Chạy `python -m src.task4_chunking_indexing`: **`Indexed 648 chunks`**.
- Contract tests cho Task 4–7: **5 passed**.
- Query tích hợp `du lich`: dense trả 3 kết quả, BM25 trả 3 kết quả, RRF fuse thành 3 kết quả.
- Model `BAAI/bge-m3` không tải được trong môi trường offline; đã thêm fallback embedding deterministic 1024 chiều. Khi model có local cache, Sentence Transformers vẫn được ưu tiên.

## Điều còn hạn chế

- Hash embedding có chất lượng ngữ nghĩa thấp hơn `BAAI/bge-m3`, nên dùng model thật cho đánh giá chính thức.
- BM25 corpus được nạp khi module import; tài liệu mới thêm trong cùng process cần reload hoặc cập nhật corpus.
- Chưa có benchmark định lượng riêng về recall và latency.

## Xác nhận đóng góp

Tôi xác nhận nội dung trên phản ánh đúng phần việc của mình và có thể giải thích hoặc chạy lại trong buổi demo.

- Ngày: 2026-09-25
- Tên thành viên: Nguyễn Gia Khánh
