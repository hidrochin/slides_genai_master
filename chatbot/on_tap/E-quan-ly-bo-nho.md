# E — Quản lý bộ nhớ (Long-term Memory) cho tác tử hội thoại

> Bài 9 (Quản lý lịch sử hội thoại — Ngô Văn Linh). ⇐ [ONE-PAGER](00-ONE-PAGER.md)

---

## 1. Vì sao cần bộ nhớ ngoài cho LLM?
LLM phụ thuộc **cửa sổ ngữ cảnh cố định**, **không có bộ nhớ dài hạn tự nhiên**. **Agentic AI** cần nhớ lịch sử, học từ kinh nghiệm, phối hợp đa tác nhân.
Lý do: (1) **nhất quán** hội thoại; (2) **cá nhân hoá**; (3) **theo dõi tiến trình tác vụ**; (4) hỗ trợ tác vụ đa bước/đa tác nhân; (5) **tối ưu token/độ trễ**.

**Quản lý bộ nhớ ⟺ RAG:** phân đoạn (session/chunk/turn) · phân loại (Core/episodic/semantic…) · tổ chức (tree/graph) · cập nhật (add/delete/update) · truy xuất (embedding/retrieval).

**5 hướng tiếp cận:** Segment & Compression · Multi-Granularity · Hierarchical (tree) · Graph · Multi-Agent.

## 2. Segmentation & Compression

### 2.1 Hạn chế các đơn vị nhớ
- **Turn-level**: nhỏ, chi tiết, nhưng **phân mảnh ngữ nghĩa**, dễ bỏ sót ngữ cảnh trải nhiều lượt.
- **Session-level**: **quá lớn**, nhiều phần không liên quan, nhiễu.
- **Summarization**: rút gọn nhưng dễ **bỏ chi tiết quan trọng**.
→ Giải pháp: phân đoạn theo **chủ đề (topic)**.

### 2.2 SeCom (ICLR 2025) ⭐
Hai khối: **SE** (Segmentation) + **COM** (Compression as Denoising).
- **SE**: phân đoạn theo **chủ đề** (không phải turn/session). Dùng **GPT-4** làm mô hình phân đoạn (mô hình nhẹ như Mistral-7B/RoBERTa cũng làm được).
- **COM**: **nén = khử nhiễu** (ngôn ngữ tự nhiên có dư thừa = nhiễu với retriever). Công cụ **LLMLingua-2** (phân loại nhị phân token: **preserve/discard**). → tăng recall, tăng tương đồng query–đoạn liên quan.
- Pipeline: offline (segment → nén → index BM25/dense + metadata) → online (retrieve top-N, ưu tiên gần thời gian nếu điểm bằng) → ghép ngữ cảnh (≤ token budget) → sinh (chỉ dựa bằng chứng, chống hallucination).

### 2.3 RMM — Reflective Memory Management (ACL 2025)
Khắc phục **phân đoạn cố định** & **retriever cố định**.
- **Prospective Reflection** (cuối mỗi phiên): trích đoạn → tóm tắt theo **chủ đề** → cập nhật memory bank (**ADD** nếu chủ đề mới, **merge** nếu mở rộng).
- **Retrospective Reflection**: **Reranker** tinh chỉnh top-K (thích ứng miền, không cần fine-tune retriever). Học bằng **RL**: reward **+1** nếu memory **được LLM trích dẫn** trong câu trả lời, **-1** nếu không. → **LLM Attribution as Rewards**.

## 3. Memory Representation Architectures
Biểu diễn phẳng (text thuần): phân mảnh, khó multi-hop. Cấu trúc (tree/graph): giữ quan hệ, truy xuất chính xác, hỗ trợ abstraction & multi-hop.

### 3.1 MemTree (Dynamic Tree Memory, ICLR 2025) ⭐
Khắc phục: **flat lookup** (SeCom/RMM/MemGPT — thiếu cấu trúc) & **static offline** (RAPTOR/GraphRAG — không cập nhật real-time).
- Cây **động**, tích hợp vào hội thoại. Nút gần gốc = tổng quát; càng sâu = càng chi tiết.
- **Mỗi nút = {content cᵥ, embedding eᵥ, parent-child links, depth dᵥ}**. Nút gốc rỗng (chỉ cấu trúc).
- **Chèn nút mới**: từ gốc, so **cosine** với các con:
  1. **Traverse Deeper** nếu rất giống 1 con (> ngưỡng).
  2. **New Leaf** nếu không đủ giống.
  3. **Expand Leaf** nếu dừng ở lá → nâng cấp thành nút cha.
- **Ngưỡng thích ứng**: `θ(d) = θ₀·e^(λd)` — càng sâu ngưỡng càng cao (chỉ nhận thông tin cực liên quan).
- **Update backwards**: sau khi chèn, LLM tổng hợp nội dung cha/ông (cũ + mới). **Bảo toàn dữ liệu gốc** (không mất; nút cha chỉ chứa tóm tắt AI-generated; LLM chỉ tóm tắt dữ liệu trong cây).
- **Truy xuất — Collapsed Tree Retrieval**: "làm phẳng" cây → so query với **tất cả nút** → top-k → LLM. Kết hợp nhiều cấp trừu tượng (giống sách: nút cha = mục lục, lá = trang chi tiết).

### 3.2 Mem0 (2025) ⭐
Bền vững + tối giản (chỉ giữ **fact** cốt lõi, không giữ chunk lớn) + truy hồi có cấu trúc (multi-hop, temporal).
- Pipeline 2 pha: **Extraction** (tạo candidate memory từ cặp `(mₜ₋₁, mₜ)` + tóm tắt hội thoại S + m tin nhắn gần) → **Update**.
- **4 thao tác** (LLM quyết qua tool call): **ADD** (mới) · **UPDATE** (bổ sung/ghi đè) · **DELETE** (thông tin mới phủ định) · **NOOP** (giữ nguyên). Tham số: m=10, s=10 (top-s tương đồng), GPT-4o-mini, vector DB dense.
- **Mem0g** = biểu diễn **đồ thị**: `G=(V,E,L)`, node=thực thể (embedding + type + timestamp), edge=quan hệ (vs, r, vd). LLM sinh triple. Xung đột → LLM đánh dấu **invalid** (không xoá). Truy xuất **entity-centric** + **semantic triplet**. DB: **Neo4j**.

## 4. Graph & Multi-Granularity Memory

### 4.1 HippoRAG 2 (ICML 2025)
(chi tiết ở [D-graphrag-lightrag](D-graphrag-lightrag.md)) — OpenIE triples + phrase(sparse)/passage(dense) nodes + **Personalized PageRank** + query-to-triple. Non-parametric continual learning.

### 4.2 MaGiX (EMNLP 2025) — Cross-Lingual RAG
Đa mức + đa ngôn ngữ. Vấn đề **canonicalization** (LLM sinh nhiều tên cho 1 thực thể: "Hanoi", "Thăng Long", "Kẻ Chợ").
- Mỗi thực thể có **nhiều ngữ cảnh** → embedding riêng mỗi ngữ cảnh (không mất thông tin như LightRAG).
- **Cousin edge** (đồng nghĩa): nếu `cosine(vᵢₖ, vⱼₗ) > τ` → thêm cạnh đồng nghĩa (kể cả **xuyên ngôn ngữ**).
- Fine-tune 2 giai đoạn: (1) **contrastive** tự giám sát; (2) có giám sát căn chỉnh xuyên ngôn ngữ (cặp song ngữ).
- Truy hồi: seed → **Cousin Expansion** → chấm điểm 3 thành phần (chunk/attr/triple) → min-max normalize → **composite score** có trọng số → top-n.

### 4.3 GNN-RAG (ACL 2025)
Kết hợp **GNN + LLM** cho **KGQA**.
- **GNN = bộ xử lý đồ thị** (message passing có điều kiện theo câu hỏi `ω(q,r)`), phân loại node "đáp án/không". Reset tại `l=L/2`. Chọn node xác suất tích luỹ > 0.95.
- Trích **đường đi ngắn nhất** từ thực thể câu hỏi → ứng viên → **verbalize** (thành văn bản) → context cho **LLM = bộ suy luận** (Llama-7B-Chat + prompt tuning).

### 4.4 MemGAS (2025) — Multi-Granularity Memory Association & Selection
- Mỗi phiên → **4 nút**: `Mᵢ = {Sᵢ (session), Tᵢ (turn), Uᵢ (summary), Kᵢ (keyword)}`. Lưu ý `e(Sᵢ) ≠ e(Tᵢ)` (S mã hoá toàn văn 1 lần; T = mean-pool embedding từng lượt).
- **Dynamic Memory Association**: memory mới liên kết memory cũ; dùng **Gaussian Mixture Model (GMM)** chia Accept Set / Reject Set.
- **Entropy-based Router**: với truy vấn q, tính entropy Shannon của phân phối tương đồng ở mỗi mức → **trọng số mềm** `wg = (1/Hg)/Σ(1/Hg')` (entropy thấp = chắc chắn = trọng số cao) → tự chọn mức nhớ.
- **Personalized PageRank** trên đồ thị liên kết → top-K → **LLM redundancy filtering** (loại trùng lặp).

## 5. Agent Memory Manager
Agent làm "API" giữa LLM & bộ nhớ; tách lớp **hot (ngắn hạn) / warm (tóm tắt) / cold (lâu dài)**.
Chức năng: **Insert · Delete · Update · Retrieve · Summarize**.

### 5.1 MemGPT (2024) — LLM as Operating System ⭐
Vấn đề: context window giới hạn (chi phí self-attention **bậc hai**; **"lost in the middle"**).
- **Ảo giác ngữ cảnh vô hạn** qua **Virtual Context Management** (giống **paging** của OS).
- Kiến trúc phân cấp:
  - **Main Context (≈ RAM)**: **System Instructions** (read-only) + **Working Context** (đọc/ghi: fact, sở thích, mục tiêu) + **FIFO Queue** (tin nhắn gần nhất).
  - **External Context (≈ Disk)**: **Recall Storage** (toàn bộ lịch sử, tìm được) + **Archival Storage** (tài liệu, file lớn).
- **LLM = CPU**: tự quyết đọc/ghi qua **function calls** (như system calls). **Event-driven** (tin nhắn, cảnh báo **Memory Pressure** khi FIFO gần đầy, timed events). Có runtime error feedback loop + pagination.

### 5.2 MIRIX (2025) — Multi-Agent Memory ⭐ (SOTA LOCOMO)
Khắc phục: thiếu cấu trúc/abstraction, kém multi-modal, kém mở rộng, **stateless**.
- **6 module bộ nhớ** (cảm hứng trí nhớ người) ⭐:
  1. **Core Memory** — thông tin bền vững (tên, sở thích), luôn trong ngữ cảnh.
  2. **Episodic Memory** — nhật ký sự kiện theo thời gian.
  3. **Semantic Memory** — kiến thức/khái niệm/sự thật ("Hà Nội là thủ đô VN").
  4. **Procedural Memory** — hướng dẫn từng bước ("cách commit code").
  5. **Resource Memory** — tài liệu/file/media.
  6. **Knowledge Vault** — thông tin **nhạy cảm** (mật khẩu, API keys).
- **Multi-Agent**: **Meta Memory Manager** (định tuyến) + 6 **Memory Managers** + **Chat Agent**. Hỗ trợ **multi-modal** + **Active Retrieval** (tự nhận diện chủ đề → gọi tool).

## 6. Datasets & Metrics
- **LOCOMO** ⭐: chuẩn đánh giá nhớ dài hạn; **10 hội thoại**, TB **~600 lượt / ~26k token**. Câu hỏi: **single-hop · multi-hop · temporal · open-domain**.
- **Long-MT-Bench+**: gộp 5 phiên; GPT-4 sinh câu hỏi ngữ cảnh dài.
- **LongMemEval (s/m)**: s = 50 phiên/câu (~103k token); m = 500 phiên/câu (~1tr token) — test scalability.
- **MSC / MSC-E**: hội thoại đa phiên, persona nhất quán. MSC ~15 lượt; **MSC-E ~200 lượt** (MemTree tạo). MemGPT có tác vụ **DMR (Deep Memory Retrieval)**.
- **Metric QA**: F1, BLEU, ROUGE, BERTScore + **LLM-as-a-Judge** (GPT4Score / J Score — tin cậy nhất). **Retrieval**: **Recall@k**, **NDCG@k**.
- Kết quả LOCOMO (J Score): Full-Context 72.9 · Mem0(Graph) 68.4 · **MIRIX 85.4** (cao nhất).

---
## ✅ Chốt nhanh mục E
- Đơn vị nhớ: turn (phân mảnh) < session (nhiễu) → phân đoạn theo **chủ đề**.
- **SeCom** = Segment (GPT-4) + Compress (**LLMLingua-2**, khử nhiễu). **RMM** = Prospective + Retrospective (**RL**, reward = được trích dẫn).
- **MemTree** = cây động, ngưỡng `θ₀e^(λd)`, Collapsed Retrieval. **Mem0** = fact + **ADD/UPDATE/DELETE/NOOP**; Mem0g = graph (Neo4j).
- **MemGPT** = LLM as OS (RAM↔Disk, paging, function call). **MIRIX** = 6 module + multi-agent (SOTA LOCOMO 85.4).
- Benchmark: **LOCOMO** (600 lượt/26k) · metric = LLM-as-a-Judge + Recall@k/NDCG@k.
