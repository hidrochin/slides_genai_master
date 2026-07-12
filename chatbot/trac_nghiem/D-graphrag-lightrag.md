# Trắc nghiệm D — GraphRAG, LightRAG & HippoRAG 2

> Lý thuyết: [on_tap/D-graphrag-lightrag](../on_tap/D-graphrag-lightrag.md). Đáp án cuối file.

---

**1.** Hai loại câu hỏi mà RAG thường (vector) hay FAIL, GraphRAG khắc phục:
A. Yes/no và factoid
B. Multi-hop reasoning và Query-Focused Summarization (QFS)
C. Definition và comparative
D. Opinion và procedural

**2.** Multi-hop reasoning question là:
A. Câu hỏi trả lời được từ 1 chunk duy nhất
B. Câu hỏi cần nhiều đoạn + suy luận nhiều bước
C. Câu hỏi yes/no
D. Câu hỏi tóm tắt

**3.** Thay vì lưu vector DB, GraphRAG:
A. Dựng Knowledge Graph từ raw documents
B. Dùng BM25 thuần
C. Fine-tune LLM
D. Nén tài liệu

**4.** Khi trích relationship, GraphRAG lưu thêm thuộc tính nào ngoài mô tả?
A. relationship_strength (điểm số)  B. timestamp  C. language  D. author

**5.** Thuật toán phát hiện cộng đồng (community detection) dùng trong GraphRAG:
A. K-means  B. Louvain thuần  C. Leiden (phân cấp)  D. DBSCAN

**6.** Global search (trả lời câu hỏi QFS) trong GraphRAG dùng cơ chế:
A. Map-Reduce trên community reports
B. Single vector lookup
C. BM25 rerank
D. Regex matching

**7.** Trong bước Map của Global search, mỗi điểm chính được gán:
A. Importance Score (0-100)  B. Nhãn BIO  C. Embedding  D. URI

**8.** Local search trong GraphRAG phù hợp cho:
A. Câu hỏi tóm tắt toàn cục
B. Câu hỏi cụ thể về thực thể (dùng entity + neighbor)
C. Câu hỏi yes/no
D. Không dùng graph

**9.** Vấn đề chính của GraphRAG mà LightRAG giải quyết:
A. Không hỗ trợ tiếng Việt
B. Chi phí dựng hierarchical graph + global query rất đắt, khó thích ứng dữ liệu mới
C. Không trích được entity
D. Không dùng LLM

**10.** LightRAG bỏ thành phần nào để giảm chi phí?
A. Vector store  B. Hierarchical graph  C. LLM  D. Embedding

**11.** Dual-level retrieval của LightRAG gồm:
A. Low-level (cụ thể) và High-level (trừu tượng)
B. Dense và sparse
C. Local và session
D. Turn và chunk

**12.** Trong LightRAG, low-level keywords khớp với thành phần nào của KG?
A. candidate relations (edges)
B. candidate entities (nodes)
C. community reports
D. passages

**13.** High-level keywords của LightRAG tập trung vào:
A. Thực thể cụ thể, chi tiết
B. Khái niệm/chủ đề bao quát
C. Số liệu
D. Tên riêng

**14.** HippoRAG 2 lấy cảm hứng từ:
A. Lý thuyết hippocampal indexing của trí nhớ dài hạn con người
B. Thuật toán PageRank cổ điển
C. Kiến trúc Transformer
D. Mô hình GAN

**15.** Thuật toán lan truyền trọng số dùng trong HippoRAG 2:
A. Personalized PageRank (PPR)
B. Dijkstra
C. A*
D. Beam search

**16.** HippoRAG 2 thêm loại node nào để mã hoá ngữ cảnh (dense) bên cạnh phrase node (sparse)?
A. Passage nodes (cạnh "contains")
B. Community nodes
C. Summary nodes
D. Root node

**17.** HippoRAG 2 thay NER-to-node bằng phương pháp mặc định nào để có ngữ cảnh phong phú hơn?
A. Query-to-triple  B. Keyword matching  C. BM25  D. Regex

**18.** Prompt "Summarize description" (Prompt 2) trong GraphRAG dùng để:
A. Trích entity
B. Gộp nhiều mô tả của cùng thực thể thành 1 mô tả thống nhất
C. Phát hiện cộng đồng
D. Map-reduce

**19.** Community summary (Prompt 3) trả về JSON gồm các trường:
A. title, summary, rating (0-10), rating_explanation, findings
B. intent, entities, slots
C. query, docs, answer
D. node, edge, weight

**20.** Phát biểu ĐÚNG khi so sánh GraphRAG và LightRAG:
A. GraphRAG có hierarchical + Leiden + global map-reduce; LightRAG bỏ hierarchical, dùng dual-level keyword
B. LightRAG đắt hơn GraphRAG
C. Cả hai đều không dùng LLM
D. GraphRAG không trích được relationship

---
### Đáp án
1-B · 2-B · 3-A · 4-A · 5-C · 6-A · 7-A · 8-B · 9-B · 10-B · 11-A · 12-B · 13-B · 14-A · 15-A · 16-A · 17-A · 18-B · 19-A · 20-A
