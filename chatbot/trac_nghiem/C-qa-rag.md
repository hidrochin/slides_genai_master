# Trắc nghiệm C — QA & RAG nâng cao

> Lý thuyết: [on_tap/C-qa-rag](../on_tap/C-qa-rag.md). Đáp án cuối file.

---

**1.** Machine Reading Comprehension (MRC) trả lời câu hỏi dựa trên:
A. Toàn bộ Wikipedia  B. Một đoạn văn bản cụ thể  C. Knowledge Graph  D. CSDL quan hệ

**2.** Trong SQuAD, câu trả lời có đặc điểm:
A. Là một câu sinh mới  B. Là một span (xâu ngắn) trong đoạn văn  C. Là yes/no  D. Là số điểm

**3.** Open-Domain QA khác MRC ở chỗ:
A. Không cho trước 1 đoạn, phải tìm trên kho lớn (Wikipedia)
B. Chỉ trả lời yes/no
C. Không dùng embedding
D. Chỉ hoạt động offline

**4.** BM25 thuộc loại truy xuất nào?
A. Dense/semantic  B. Sparse/lexical  C. Multi-vector  D. Graph-based

**5.** Hạn chế của BM25:
A. Quá chậm  B. Không xét ngữ nghĩa/ngữ cảnh, giả định từ độc lập  C. Cần GPU  D. Không chuẩn hoá độ dài

**6.** Bi-encoder khác cross-encoder ở điểm nào?
A. Bi-encoder mã hoá Q và D độc lập, precompute được embedding
B. Bi-encoder ghép Q+D vào chung 1 model
C. Bi-encoder luôn chính xác hơn
D. Bi-encoder chậm hơn cross-encoder

**7.** Kiến trúc thường dùng để **re-rank** (chính xác cao, chậm) là:
A. Bi-encoder  B. Cross-encoder  C. BM25  D. TF-IDF

**8.** BGE-M3 được xây trên mô hình nền nào và max token bao nhiêu?
A. BERT-base, 512  B. XLM-RoBERTa, 8192  C. GPT-2, 1024  D. T5, 2048

**9.** "Multi-functionality" của BGE-M3 nghĩa là hỗ trợ:
A. Chỉ dense retrieval
B. Dense + lexical/sparse + multi-vector retrieval
C. Chỉ tiếng Anh
D. Chỉ câu ngắn

**10.** Kỹ thuật huấn luyện đặc trưng của BGE-M3:
A. Reinforcement learning  B. Self-knowledge distillation  C. Adversarial  D. Federated learning

**11.** Multi-Query trong Query Translation:
A. Sinh nhiều biến thể câu hỏi để retrieve đa dạng hơn
B. Thêm re-ranker
C. Chuyển câu hỏi thành SQL
D. Nén ngữ cảnh

**12.** Điểm khác biệt của RAG-Fusion so với Multi-Query:
A. Không sinh biến thể  B. Thêm Re-ranker (giảm lost-in-the-middle)  C. Dùng graph  D. Bỏ retriever

**13.** HyDE (Hypothetical Document Embeddings) hoạt động bằng cách:
A. Sinh câu hỏi tổng quát hơn
B. Sinh câu trả lời giả định rồi embed để retrieve tốt hơn
C. Chia câu hỏi thành sub-question
D. Định tuyến câu hỏi

**14.** Step-back prompting nghĩa là:
A. Sinh câu hỏi tổng quát/generic hơn (dễ trả lời hơn) trước
B. Sinh answer giả
C. Nén tài liệu
D. Web search

**15.** Parent Document Retriever giải quyết vấn đề:
A. Cân bằng embedding chính xác (chunk nhỏ) với ngữ cảnh đầy đủ (doc cha)
B. Dịch câu hỏi
C. Xếp hạng
D. Nén prompt

**16.** Vấn đề "Lost in the middle" xảy ra khi:
A. Câu hỏi quá ngắn
B. Ngữ cảnh dài, thông tin ở giữa dễ bị bỏ sót
C. Không có retriever
D. Dùng BM25

**17.** Corrective-RAG (CRAG) làm gì khi không tìm được tài liệu liên quan?
A. Trả lời "không biết" ngay
B. LLM re-write câu hỏi rồi web search
C. Tăng số chunk
D. Đổi embedding model

**18.** Self-RAG đặc trưng bởi:
A. LLM tự phản tỉnh (self-critique), quyết định khi nào retrieve & đánh giá chất lượng
B. Chỉ dùng BM25
C. Không dùng LLM
D. Chỉ dịch câu hỏi

**19.** Query Construction nhằm mục đích:
A. Chuyển ngôn ngữ tự nhiên thành cú pháp truy vấn (SQL/Cypher) cho dữ liệu có cấu trúc
B. Sinh biến thể câu hỏi
C. Nén ngữ cảnh
D. Re-rank tài liệu

**20.** Về chunk size khi indexing, phát biểu ĐÚNG:
A. Chunk lớn = nhiều ngữ cảnh nhưng nhiều nhiễu, chi phí cao
B. Chunk lớn luôn tốt hơn
C. Chunk nhỏ luôn tốt hơn
D. Kích thước chunk không ảnh hưởng

---
### Đáp án
1-B · 2-B · 3-A · 4-B · 5-B · 6-A · 7-B · 8-B · 9-B · 10-B · 11-A · 12-B · 13-B · 14-A · 15-A · 16-B · 17-B · 18-A · 19-A · 20-A
