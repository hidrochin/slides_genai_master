# Trắc nghiệm E — Quản lý bộ nhớ (Long-term Memory)

> Lý thuyết: [on_tap/E-quan-ly-bo-nho](../on_tap/E-quan-ly-bo-nho.md). Đáp án cuối file.

---

**1.** Lý do KHÔNG phải là động lực tạo bộ nhớ ngoài cho LLM:
A. Duy trì nhất quán hội thoại
B. Cá nhân hoá trải nghiệm
C. Tăng số tham số của LLM
D. Tối ưu token/độ trễ

**2.** Nhược điểm của bộ nhớ mức turn-level:
A. Quá lớn, nhiều nhiễu
B. Phân mảnh ngữ nghĩa, dễ bỏ sót ngữ cảnh trải nhiều lượt
C. Không thể index
D. Không có chi tiết

**3.** SeCom gồm hai khối chính:
A. Segmentation (SE) + Compression (COM)
B. Retriever + Generator
C. Encoder + Decoder
D. Map + Reduce

**4.** COM trong SeCom coi nén như:
A. Dịch máy  B. Khử nhiễu (denoising)  C. Tóm tắt thuần  D. Mã hoá

**5.** Công cụ nén token (preserve/discard) trong SeCom:
A. LLMLingua-2  B. BM25  C. FAISS  D. spaCy

**6.** Trong RMM, Retrospective Reflection cập nhật reranker bằng:
A. Học tăng cường (RL), reward = memory có được LLM trích dẫn không
B. Supervised learning trên nhãn người
C. K-means
D. Regex

**7.** Reward trong RMM là:
A. +1 nếu memory được trích dẫn trong câu trả lời, -1 nếu không
B. BLEU score
C. Số token tiết kiệm
D. Độ dài câu trả lời

**8.** MemTree khắc phục hạn chế của flat lookup và static structure bằng:
A. Cây tĩnh offline
B. Cây động cập nhật real-time trong hội thoại
C. Vector store phẳng
D. BM25

**9.** Một nút MemTree gồm 4 yếu tố:
A. content, embedding, parent-child links, depth
B. intent, entity, slot, action
C. query, doc, score, rank
D. node, edge, weight, label

**10.** Ngưỡng thích ứng của MemTree θ(d)=θ₀·e^(λd) có ý nghĩa:
A. Càng sâu ngưỡng càng thấp
B. Càng sâu ngưỡng càng cao (chỉ nhận thông tin cực liên quan)
C. Ngưỡng cố định
D. Ngưỡng ngẫu nhiên

**11.** Cơ chế truy xuất của MemTree:
A. Duyệt tuần tự từng nhánh
B. Collapsed Tree Retrieval (làm phẳng cây, so với tất cả nút)
C. BM25 thuần
D. Personalized PageRank

**12.** Bốn thao tác quản lý bộ nhớ của Mem0:
A. ADD, UPDATE, DELETE, NOOP
B. CREATE, READ, UPDATE, DELETE
C. PUSH, POP, PEEK, CLEAR
D. MAP, REDUCE, FILTER, SORT

**13.** Mem0g biểu diễn bộ nhớ dưới dạng:
A. Cây  B. Đồ thị có hướng gán nhãn (Neo4j)  C. Bảng phẳng  D. Danh sách liên kết

**14.** Khi phát hiện xung đột quan hệ, Mem0g xử lý bằng cách:
A. Xoá ngay quan hệ cũ
B. LLM đánh dấu quan hệ lỗi thời là invalid (không xoá)
C. Bỏ qua
D. Tạo node mới

**15.** MemGPT ví LLM như:
A. Một database  B. CPU của hệ điều hành, quản lý RAM↔Disk qua function call  C. Một retriever  D. Một compiler

**16.** Trong MemGPT, Main Context (≈ RAM) KHÔNG bao gồm:
A. System Instructions  B. Working Context  C. FIFO Queue  D. Archival Storage

**17.** MIRIX có bao nhiêu module bộ nhớ chức năng?
A. 3  B. 4  C. 6  D. 8

**18.** Module bộ nhớ MIRIX lưu thông tin nhạy cảm (mật khẩu, API key):
A. Core Memory  B. Episodic Memory  C. Semantic Memory  D. Knowledge Vault

**19.** Benchmark chuẩn đánh giá bộ nhớ dài hạn (~600 lượt, ~26k token/hội thoại):
A. SQuAD  B. LOCOMO  C. GLUE  D. ImageNet

**20.** Độ đo được xem là đáng tin cậy nhất cho chất lượng câu trả lời trong hội thoại dài:
A. Chỉ F1  B. LLM-as-a-Judge (GPT4Score / J Score)  C. Perplexity  D. Số token

**21.** Router của MemGAS chọn mức nhớ dựa trên:
A. Entropy Shannon của phân phối tương đồng (entropy thấp = trọng số cao)
B. Random
C. BM25 score
D. Độ dài câu hỏi

**22.** GNN-RAG phân chia vai trò:
A. GNN = bộ xử lý đồ thị, LLM = bộ suy luận ngôn ngữ
B. GNN sinh câu trả lời, LLM xây graph
C. Cả hai đều retrieve
D. Không dùng LLM

---
### Đáp án
1-C · 2-B · 3-A · 4-B · 5-A · 6-A · 7-A · 8-B · 9-A · 10-B · 11-B · 12-A · 13-B · 14-B · 15-B · 16-D · 17-C · 18-D · 19-B · 20-B · 21-A · 22-A
