# C — Hệ thống hỏi đáp (QA) & RAG nâng cao

> Bài 5 (L5_QA). ⇐ [ONE-PAGER](00-ONE-PAGER.md)

---

## 1. Hệ thống hỏi đáp (QA)
Mục tiêu: tự động trả lời câu hỏi bằng ngôn ngữ tự nhiên.
Nguồn: đoạn văn, web, **cơ sở tri thức (CSTT)**, CSDL, tập QA có sẵn.

**Dạng câu hỏi:** Factoid (WH: when/who/where) · Yes-No · Definition · Cause/consequence · Procedural · Comparative · Queries with examples · Opinion.
**Dạng câu trả lời:** vài từ · đoạn · danh sách · có/không.

**Các cách tiếp cận:**
- **Có bộ QA sẵn**: đo độ tương đồng câu → lấy câu trả lời của câu hỏi giống nhất (AskJeeves); hoặc học sâu.
- **Có CSDL/CSTT** (không có bộ QA): phân tích câu hỏi (ngữ nghĩa, so khớp mẫu) → tra cứu/suy diễn (TextMap, AskMSR, LCC).
- **Tìm tài liệu liên quan** → trích câu trả lời.

## 2. Các loại bài toán QA
- **Machine Reading Comprehension (MRC)**: trả lời dựa trên **1 đoạn văn cụ thể**. **SQuAD**: ~100k mẫu (đoạn–câu hỏi–trả lời), đoạn từ Wikipedia 100–150 từ, **answer = span ngắn trong đoạn**, mỗi câu hỏi 3 câu trả lời mẫu. Hạn chế: không phải câu hỏi nào cũng có answer kiểu span.
- **Open-Domain QA**: không cho trước đoạn; tìm trên **kho lớn** (Wikipedia, vector DB). Thực tế hơn nhưng khó hơn.
- **Multi-modal QA**: kết hợp nhiều loại dữ liệu (biểu đồ, ảnh y tế, video). Mô hình: **CLIP**, VisualBERT, LXMERT, ViLT, GPT-4, Flamingo, Kosmos-1, Gemini.

## 3. Retrieval cơ bản (ôn tập)
### 3.1 BM25 (Best Matching) — **sparse/lexical**
Ước lượng độ liên quan doc–query, biểu diễn giống **TF-IDF** + **chuẩn hoá độ dài tài liệu**.
- Ưu: đơn giản, hiệu quả, **nhanh**.
- Nhược: **không xét ngữ nghĩa/ngữ cảnh**, giả định **độc lập thống kê** giữa các từ.

### 3.2 Bi-encoder vs Cross-encoder ⭐
| | **Bi-encoder** | **Cross-encoder** |
|---|---|---|
| Cơ chế | mã hoá Q và D **độc lập** → so cosine | ghép Q+D vào **chung 1 model**, xử lý tương tác trực tiếp |
| Tốc độ | **nhanh** (embedding **precompute** được) | **chậm** |
| Chính xác | thấp hơn | **cao hơn** |
| Dùng cho | **retrieval** (semantic/vector search) | **re-ranking** |

### 3.3 BGE-M3 ⭐ (embedding model chủ đạo của khoá)
Nền **XLM-RoBERTa**, mở rộng max position lên **8192 token**. Giải quyết 3 thách thức embedding:
- **Multi-linguality** (đa ngôn ngữ).
- **Multi-functionality**: **Dense** retrieval + **lexical/sparse** retrieval + **multi-vector** retrieval.
- **Multi-granularity**: từ câu/đoạn ngắn đến tài liệu dài 8192 token.
- Huấn luyện: **self-knowledge distillation** + efficient batching. Kết quả re-rank theo **integrated relevance score** (kết hợp 3 loại).

## 4. RAG NÂNG CAO (pipeline chuẩn — HAY RA THI)
Thứ tự: **Query Translation → Routing → Query Construction → Indexing → Retrieval → Generation**.

### 4.1 Query Translation (dịch/biến đổi truy vấn)
Vì retrieval theo khoảng cách **nhạy cảm với cách diễn đạt** & embedding chưa hoàn hảo. Tự động hoá bằng LLM:
- **Multi-Query**: sinh **nhiều biến thể** câu hỏi → retrieve đa dạng hơn → ghép doc → hỏi LLM với câu hỏi gốc.
- **RAG-Fusion**: giống Multi-Query **NHƯNG thêm Re-ranker** đẩy doc liên quan nhất lên đầu → giảm **"Lost-in-the-middle"**.
- **Query Decomposition**: chia thành **sub-question**.
  - *Recursive*: giải tuần tự, dùng câu trả lời trước.
  - *Individual*: hỏi riêng từng sub-question → ghép (Q,A) → LLM tổng hợp.
- **Step-back**: sinh **câu hỏi tổng quát hơn** (dễ trả lời hơn) trước.
- **HyDE** (Hypothetical Document Embeddings): sinh **câu trả lời giả định** → embed nó để retrieve tốt hơn.

> **Bẫy:** Multi-Query (KHÔNG rerank) ≠ RAG-Fusion (CÓ rerank). Step-back (khái quát hoá câu hỏi) ≠ HyDE (sinh answer giả).

### 4.2 Routing
Định tuyến câu hỏi tới nguồn/prompt phù hợp (logical routing / semantic routing).

### 4.3 Query Construction
Chuyển ngôn ngữ tự nhiên → **cú pháp truy vấn** (SQL, Cypher/graph) cho **dữ liệu có cấu trúc** (trước đó embedding chỉ cho dữ liệu phi cấu trúc).

### 4.4 Indexing
Doc → segment → embedding. Chất lượng index quyết định retrieval.
- **Fixed-size chunking** (100/256/512 token): **chunk lớn** = nhiều ngữ cảnh nhưng **nhiều nhiễu, đắt**; **chunk nhỏ** = ít nhiễu nhưng ít ngữ cảnh.
- **Recursive splits & Sliding windows**: ngữ cảnh tốt hơn nhưng phức tạp.
- **Multi-Representation / Parent Document Retriever**: **embed chunk nhỏ** (chính xác) nhưng lưu **parent ID** → khi retrieve trả về **doc cha đầy đủ** (đảm bảo ngữ cảnh).
- **Specialized embeddings**: fine-tune theo miền, **ColBERT**, **bge-m3**.
- **Hierarchical Indexing** (index phân cấp).

### 4.5 Retrieval
Nguồn (phi/có cấu trúc, LLM-generated) & **độ hạt (granularity)** ảnh hưởng kết quả: Token < Phrase < Sentence < Proposition < Chunk < Document.
- **Corrective-RAG (CRAG)**: node **grade** kiểm tra doc liên quan hay không; nếu không có doc liên quan → LLM **re-write câu hỏi** → **web search**.

### 4.6 Generation
Không nên nhét thẳng tất cả doc vào LLM. Vấn đề: **dư thừa** & **"Lost in the middle"** với ngữ cảnh dài.
Giải pháp:
- **Reranking**: ColBERT, reranker models.
- **Context compression**: dùng LM nhỏ loại bỏ từ ít thông tin.
- **Self-RAG**: LLM **tự phản tỉnh (self-critique)** — quyết định khi nào retrieve, đánh giá độ liên quan & chất lượng câu trả lời.

---
## ✅ Chốt nhanh mục C
- MRC (1 đoạn, SQuAD, answer=span) vs Open-domain (kho lớn) vs Multi-modal.
- BM25 (sparse, không ngữ nghĩa) · Bi-encoder (retrieve, nhanh, precompute) · Cross-encoder (rerank, chính xác, chậm).
- **BGE-M3** = XLM-RoBERTa, 8192 token, Multi-lingual/functionality/granularity, self-knowledge distillation.
- RAG nâng cao: Multi-Query/**RAG-Fusion**(rerank)/Step-back/**HyDE** · Parent Document Retriever · **CRAG**(grade→websearch) · **Self-RAG**(critique) · chống **lost-in-the-middle** (rerank + compression).
