# CHEAT-SHEET — Cụm E: Transformer Đa thể thức & Suy luận có Cấu trúc (Thách thức 3)
Nguồn: `lecture5_1-MultimodalTransformers-Part1`, `lecture6_1-MultimodalTransformers-Part2`, `Lecture5_2-StructuredRepresentationsAndReasoning`. (Nền self-attention/BERT xem [D-alignment](D-alignment.md).)

---

## 1. KHỐI TRANSFORMER ENCODER (nhắc lại nhanh)
`Input embeddings → Multi-Head Self-Attention → Add&Norm → Feed-Forward Network → Add&Norm → Contextualized embeddings`.
- **Attention** trộn thông tin giữa token; **FFN** biến đổi từng token; **Add&Norm** (residual + layernorm) ổn định train & giúp gradient.
- **Input = token embedding + position embedding + segment embedding** (what / where / which-sentence).

---

## 2. TRANSFORMER ĐA THỂ THỨC — 3 mẫu thiết kế ⭐⭐⭐ (rất hay hỏi)

| Mẫu | Cơ chế | Ví dụ điển hình |
|---|---|---|
| **One-stream (concatenate)** | Nối mọi modality thành **1 chuỗi**, full self-attention chung | **VisualBERT, UNITER** |
| **Cross-modal (two-stream)** | Các luồng **riêng** trao đổi qua **cross-attention / co-attention** | **ViLBERT, LXMERT** |
| **Modality-shift** | Modality phụ **dịch (shift)** biểu diễn modality chính | **MAG-BERT** |

### 2.1. One-stream: VisualBERT / UNITER
- Text token + image region → **một chuỗi chung** `[CLS] text [SEP] region1 region2...` → shared transformer, **full self-attention across text & image**.
- **VisualBERT** = baseline kiểu BERT; **UNITER** = mục tiêu phong phú hơn (masked word, masked region, image-text matching, dùng cả **optimal transport** cho word-region alignment).

### 2.2. Cross-modal: ViLBERT / LXMERT ⭐
- **Cross-modal attention:** Query từ modality **cần cập nhật**, Key/Value từ modality kia. VD **V→L** (visually contextualize language): `α = softmax(Q_L K_V^T/√d)`, output = biểu diễn ngôn ngữ **được ngữ cảnh hóa bằng thị giác** + residual.
- **ViLBERT:** 2 luồng (language stream + vision stream) trao đổi qua **co-attention layers**.
- **LXMERT:** unimodal encoders **trước**, rồi **cross-modality encoder**.
- Cả hai: **luồng riêng + cross-modal attention**.

### 2.3. Modality-shift: MAG-BERT
- **MAG (Multimodal Adaptation Gate) + BERT:** thêm một **dịch chuyển đa thể thức học được** vào hidden state của BERT. Tín hiệu thị giác/giọng nói **dịch nghĩa** từ ngôn ngữ: "great" + cười/giọng phấn khích → tích cực; + mỉa mai/giọng đều → tiêu cực.

---

## 3. VISION & VIDEO TRANSFORMERS

### 3.1. ViT (Vision Transformer, Dosovitskiy 2020) ⭐
- "An image is worth 16×16 words": chia ảnh thành **patch 16×16** → flatten → coi như **token** → transformer + position embedding + token `[CLS]` cho embedding cả ảnh.
- **CNN vs Transformer:** conv có **inductive bias locality** (data-efficient, ít data thắng); ViT **không có bias locality** → cần **pretrain quy mô lớn** nhưng long-range trực tiếp + attention động.
- **Visual tokens:** DALL-E dVAE (grid 32×32, mỗi ô là 1 "visual token" trong [0..8191]); **BeiT** = BERT pretraining cho ảnh (dự đoán visual token bị mask).

### 3.2. MAE (Masked Auto-Encoder, He 2022) ⭐
- Mask **~70–75%** patch ngẫu nhiên → encoder (ViT) chỉ xử lý patch **thấy được** → decoder nhẹ tái tạo patch bị mask (**reconstruction loss chỉ trên patch mask**). Decoder **chỉ dùng khi pretrain**. Tỉ lệ mask cao → task khó, học biểu diễn tốt & train hiệu quả.

### 3.3. Vision-Language transformers ⭐
- **ViLT (≈ ViT + BERT):** bỏ region detector nặng — patch ảnh + text token vào chung 1 transformer → **inference nhanh**; dùng optimal transport cho alignment.
- **ALBEF (Align **before** Fuse):** **căn (contrastive) segment-level TRƯỚC**, rồi mới fuse; liên hệ mutual information + momentum distillation.
- **VLC (Vision-Language from Captions):** thêm ngôn ngữ vào MAE.
- **DETR/MDETR:** transformer set-prediction cho detection (từ ảnh + text).

### 3.4. Video transformers (weakly-paired data)
- **HowTo100M:** clip ngắn (~3.2s, 32 frame) + ít từ (≤16) — **weakly paired** → **multi-instance learning + contrastive learning** (Miech 2020).
- **VideoBERT (Sun 2019):** **K-means clustering** → "visual words" cho video; **ActBERT:** global-local video-text.

---

## 4. VƯỢT RA NGOÀI CHUỖI — Structured Representations ⭐⭐

**Câu hỏi cốt lõi:** transformer nối **mọi token với mọi token** (fully-connected) — nhưng nếu có **tri thức miền về kết nối** thì sao? → dùng cấu trúc **graph / tree / module**.

### 4.1. Graph Neural Networks (GNN) ⭐⭐
- **Bài toán:** node có nhãn (supervised: human-or-bot) hoặc học embedding (unsupervised). `G = (V, A, X, Y)`.
- **Ý tưởng cốt lõi:** sinh **node embedding** từ **neighborhood cục bộ theo cách đệ quy** — mỗi node có **computation graph riêng**; nhiều tầng; **chia sẻ tham số trong 1 tầng**; layer-0 = feature `x_u`.
- **Neighborhood aggregation** — cách gộp hàng xóm:
  - **Average pooling / GraphSAGE** (Scarselli 2005): trọng số khác nhau cho self vs neighbor.
  - **GCN (Kipf 2017):** cùng trọng số, khác normalization; hiệu quả.
  - **GAT (Graph Attention Network, Veličković 2018):** **trọng số attention `α_uv`** cho từng hàng xóm.
- 👉 **GNN rất giống self-attention transformer** — transformer = GNN trên **đồ thị đầy đủ (fully-connected)**.

### 4.2. Hierarchical structure
- Khai thác **cây cú pháp** ngôn ngữ để grounding: parse → object detection → **coordination** → **composition** (VD "Skis of man in red jacket" — Hong 2019). Cùng ý với TreeRNN nhưng cho vision-language.

### 4.3. Modular structure — Neural Module Networks ⭐⭐
- **NMN V1 (Andreas 2016):** phân tích câu hỏi thành **layout tính toán** gồm các **module** (Attend, Combine, Measure...). VD "Is the bus full of passengers?" → Attend(bus) + Attend(full) → Combine(and) → Measure(is). Mỗi module xử lý attention map. **CLEVR** (Johnson 2017) là dataset chuẩn cho visual reasoning hợp thành.
- **NMN V2 (Hu 2017, End-to-End):** dùng **RNN dự đoán layout** (policy) — **không cần parse câu hỏi**, không cần luật thủ công tạo layout.
- **NMN V3 — Neuro-Symbolic VQA (Yi 2018):** (1) trích **thuộc tính ảnh** (symbolic scene), (2) **parse câu hỏi thành program**, (3) **thực thi program** trên biểu diễn symbolic của ảnh → **tách suy luận khỏi nhận thức thị giác/ngôn ngữ**.
- **NMN V4 — Neural State Machine (Hudson & Manning 2019):** (1) sinh **probabilistic scene graph** (alphabet khái niệm/quan hệ pretrain từ Visual Genome), (2) coi graph như **state machine**, (3) dịch câu hỏi thành **soft instructions** → **suy luận tuần tự** trên scene graph.

---

## 5. MEMORY cho chuỗi đa thể thức
- Vision-and-Language Navigation: **memory + aligned contextualized representations** trả lời "tôi đã tới đâu?" (History Aware Multimodal Transformer; variable-length memory).

---

## 🎯 CÂU HAY RA THI (Cụm E)
1. 3 mẫu transformer đa thể thức + ví dụ mỗi loại? (one-stream: VisualBERT/UNITER; cross-modal: ViLBERT/LXMERT; modality-shift: MAG-BERT).
2. Cross-modal attention V→L: Query lấy từ modality nào? (từ modality **cần cập nhật** = language).
3. ViT chia ảnh thế nào? Vì sao ViT cần pretrain lớn hơn CNN? (không có bias locality).
4. MAE mask bao nhiêu %? Decoder dùng khi nào? Loss ở đâu?
5. ViLT ≈ gì? ALBEF nhấn mạnh điều gì? (align before fuse).
6. GNN sinh embedding thế nào? GCN vs GAT khác gì? Transformer = GNN trên đồ thị nào?
7. NMN V1→V4 tiến hóa ra sao? Neuro-symbolic VQA tách gì khỏi gì?
8. VideoBERT tạo "visual words" bằng gì? (K-means clustering).
