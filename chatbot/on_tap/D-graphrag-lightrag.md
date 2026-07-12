# D — GraphRAG, LightRAG & HippoRAG 2

> Bài 7 (Structured-GraphRAG). ⇐ [ONE-PAGER](00-ONE-PAGER.md)

---

## 1. Vì sao cần GraphRAG?
LLM yếu ở: **Knowledge Cutoff** (không biết thông tin mới) & **Hallucination** (bịa). RAG khắc phục bằng truy xuất nguồn ngoài.
**NHƯNG** RAG thường (embedding đoạn văn phi cấu trúc → cosine) chỉ lấy được thông tin **nằm cục bộ trong 1 chunk** → **FAIL** ở 2 loại câu hỏi:
1. **Multi-hop reasoning**: cần **nhiều đoạn + suy luận nhiều bước**. *(VD: "CLB mà Ronaldo chơi tiền đạo năm 2017 được thành lập khi nào?" → cần đoạn 1 (Ronaldo→Real Madrid) + đoạn 2 (Real Madrid thành lập 1902)).*
2. **Query-Focused Summarization (QFS)**: trích ý chính từ toàn bộ tập dữ liệu ("chủ đề chính của cuốn sách là gì?").

**Structured-GraphRAG**: thay vì lưu vector DB, **dựng Knowledge Graph** từ raw documents → cho phép **multi-hop reasoning** trên graph + graph phân cấp nén tri thức → giải quyết cả QFS lẫn multi-hop.

## 2. GraphRAG: From Local to Global (Microsoft) ⭐
Paper: *From Local to Global: A Graph RAG Approach to QFS*. Pipeline offline → online:

### 2.1 Chunking
Chia document dài → text chunks nhỏ.

### 2.2 Trích entity + relationship → build graph (bằng LLM prompt)
- **Entity**: `(entity_name [viết hoa], entity_type, entity_description)`.
- **Relationship**: `(source_entity, target_entity, relationship_description, relationship_strength [điểm số])`.
> VD: "Hồ Chí Minh đọc Tuyên ngôn Độc lập tại Quảng trường Ba Đình 1945" → entity: HỒ CHÍ MINH (PERSON), TUYÊN NGÔN ĐỘC LẬP (EVENT), QUẢNG TRƯỜNG BA ĐÌNH (LOCATION); relationship: (HỒ CHÍ MINH → TUYÊN NGÔN ĐỘC LẬP, strength 8).
- **Prompt 2 — Summarize description**: gộp nhiều mô tả của cùng thực thể/nhóm thành **1 mô tả thống nhất** (giải quyết mâu thuẫn, ngôi thứ 3, giới hạn độ dài).

### 2.3 Tạo Graph Communities & Community Summaries
- **Leiden community detection** (Traag 2019, kế thừa Louvain) theo **phân cấp** (recursive) đến leaf communities không chia được nữa.
- **Community summaries** (báo cáo cộng đồng):
  - **Leaf-level**: ưu tiên theo **edge importance** (rank theo tổng bậc source+target); thêm mô tả node + edge + claim đến khi đầy context window.
  - **Higher-level**: nếu không vừa → thay element summaries dài bằng **sub-community summaries** ngắn hơn.
  - **Prompt 3**: sinh báo cáo JSON: `title, summary, rating (0-10 impact), rating_explanation, findings[]`.

### 2.4 Từ Community → Global Answer (QFS): **MAP-REDUCE** ⭐
- **Map**: mỗi community report → sinh **danh sách điểm chính** kèm **Importance Score (0-100)** (Prompt 4). "Không biết" → score 0.
- **Reduce**: tổng hợp các báo cáo (xếp theo độ quan trọng giảm dần) → **câu trả lời cuối** (Prompt 5). Không bịa.
- **Local search**: cho câu hỏi cụ thể về thực thể (dùng entity + neighbor); **Global search**: cho QFS. (**Glocal** = kết hợp).

## 3. LightRAG ⭐ (hiệu quả + thích ứng)
**Vấn đề của GraphRAG:** chi phí/thời gian dựng **hierarchical graph** + global query **rất đắt**; khó thích ứng dữ liệu mới.

**LightRAG:**
- **Bỏ hierarchical graph** → giảm nhiều chi phí.
- **Fast adaptation**: tích hợp dữ liệu mới mượt (incremental) → giảm computational overhead.
- **Dual-level retrieval paradigm** ⭐:
  - **Low-Level Retrieval** ~ câu hỏi **cụ thể** (thực thể/chi tiết).
  - **High-Level Retrieval** ~ câu hỏi **trừu tượng** (khái niệm/chủ đề).
- Cơ chế: trích **high-level & low-level keywords** (Prompt 6, output JSON) → **keyword matching** với node/edge trong KG:
  - Local keywords ↔ **candidate entities** (nodes).
  - Global keywords ↔ **candidate relations** (edges).
  - Gom **neighboring nodes** trong local subgraph (incorporating high-order relatedness).
- Kết hợp **graph + vectors**.

> **Bẫy so sánh:** GraphRAG (hierarchical + Leiden + map-reduce global, đắt) vs **LightRAG** (bỏ hierarchical, dual-level keyword, rẻ + adaptive).

## 4. HippoRAG 2
Cảm hứng **hippocampal indexing theory** của trí nhớ dài hạn con người (mô phỏng **neocortex + hippocampus**).
- Xây KG bằng **OpenIE**: LLM trích **triples** (chủ ngữ–quan hệ–tân ngữ); chủ ngữ/tân ngữ = **phrase nodes**; thêm **synonym edge** khi cặp phrase có độ tương đồng vector vượt ngưỡng.
- **Dense-Sparse Integration**: phrase nodes = **sparse** (khái niệm); thêm **passage nodes = dense** (ngữ cảnh); cạnh **"contains"** nối passage ↔ phrase.
- Truy hồi online: query → link tới triples & passages (embedding) → **seed nodes** → **recognition memory** (LLM lọc top-k triples) → **Personalized PageRank (PPR)** lan truyền → xếp hạng passage → context cho QA.
- Cải tiến: bỏ **NER-to-node** thuần, dùng **query-to-triple** (ngữ cảnh phong phú hơn) làm mặc định → **context-aware retrieval**.

---
## ✅ Chốt nhanh mục D
- RAG thường fail: **multi-hop** & **QFS** → GraphRAG dựng **KG**.
- GraphRAG: chunk → trích entity/relationship (description + strength) → **Leiden** communities phân cấp → community summaries → **Global = Map-Reduce**, **Local** cho câu hỏi cụ thể.
- **LightRAG**: bỏ hierarchical (rẻ, adaptive) + **dual-level** (low=cụ thể, high=trừu tượng) + keyword matching.
- **HippoRAG 2**: OpenIE triples + phrase(sparse)+passage(dense) + **PPR** + query-to-triple.
