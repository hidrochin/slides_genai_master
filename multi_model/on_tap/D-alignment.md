# CHEAT-SHEET — Cụm D: Alignment & Biểu diễn Căn chỉnh (Thách thức 2)
Nguồn: `lecture4.1-MultimodalAlignment`, `lecture4.2-AlignedRepresentations`. Bao gồm 3 sub-challenge của Alignment + nền tảng **self-attention/BERT** (dùng lại cho Cụm E).

> **Định nghĩa Alignment:** *Nhận diện & mô hình hóa kết nối chéo giữa **mọi phần tử** của nhiều modality, xây từ cấu trúc dữ liệu.* 3 sub-challenge: **Discrete alignment** (phần tử rời rạc) · **Continuous alignment** (segmentation + warping) · **Contextualized representation** (alignment + representation).

---

## 1. DISCRETE ALIGNMENT — kết nối các phần tử rời rạc

**Trục phân loại:** Local vs Global · Undirected vs Directed.

### 1.1. Language grounding & Local alignment
- **Grounding:** gắn ngôn ngữ (từ/cụm từ) với phần tử phi ngôn ngữ (đối tượng thị giác). VD "a woman reading newspaper" → vùng ảnh.
- **Local alignment** = coordinated representations / contrastive learning trên **cặp phần tử** (cần paired data), dùng similarity `g(z_A,z_B)`.

### 1.2. Directed alignment = ATTENTION (hard vs soft) ⭐
Query (modality A) → Key (modality B), "which object?":
| | **Soft attention** | **Hard attention** |
|---|---|---|
| Chọn | phân phối trên **tất cả** vị trí (weighted average) | **1** vị trí rời rạc (sampled glimpse) |
| Train | **khả vi end-to-end** | cần sampling (thường **RL**) |
| Dùng | mặc định trong seq2seq/transformer | khi hạn chế tính toán |
- Ví dụ: **Show, Attend and Tell** (Xu 2015) image captioning; **Recurrent Models of Visual Attention** (Mnih 2014, hard).

### 1.3. Global alignment = ASSIGNMENT & OPTIMAL TRANSPORT ⭐⭐
- **Assignment problem:** ghép **1-1 cứng** giữa 2 tập **cùng kích thước** (perfect matching). Maximize `Σ w(i,f(i))` với `w(i,j)=g(z_A^i, z_B^j)`. Giải bằng **Linear Programming / simplex / Hungarian** (không cần duyệt toàn bộ). `x_ij ∈ {0,1}`.
- **Optimal Transport (OT):** ghép **mềm, many-to-many**, tập **kích thước khác nhau**, correspondence một phần. `x(i,j) ≥ 0` (mass có thể chia). Xem như "vận chuyển" phần tử A→B; **Wasserstein distance** cho lời giải tối ưu.
- **Quy tắc chọn:** mỗi phần tử cần đúng 1 partner + tập bằng nhau → **assignment**; ghép một phần/không đều/mềm → **OT**.

---

## 2. CONTINUOUS ALIGNMENT — tín hiệu liên tục, không có phần tử rõ ràng

### 2.1. Dynamic Time Warping (DTW) ⭐⭐
- Hai tín hiệu thời gian chưa căn `X ∈ ℝ^{d×n_x}`, `Y ∈ ℝ^{d×n_y}`; tìm cặp vector chỉ số `(p_x, p_y)` **cùng độ dài** để minimize `Σ_t ‖x_{p_x,t} − y_{p_y,t}‖²`.
- = **đường chi phí thấp nhất** trong ma trận cost, giải bằng **quy hoạch động** với các **ràng buộc**: **monotonicity** (không lùi thời gian) · **continuity** (không nhảy cách) · **boundary** (bắt đầu/kết thúc trùng) · **warping window** (không quá xa đường chéo) · **slope constraint** (không chèn/bỏ quá nhiều).
- **Dạng ma trận:** `L(W_x,W_y) = ‖X·W_x − Y·W_y‖²_F` (W = ma trận căn chỉnh, Frobenius norm).

### 2.2. Họ DTW ⭐
| | Đặc điểm | Khi dùng |
|---|---|---|
| **DTW** | 1 đường tối ưu qua cost matrix | căn thời gian, timing là vấn đề chính |
| **Soft-DTW** (Cuturi 2017) | soft-min → **khả vi** | dùng làm **loss** trong model train được |
| **CTW (Canonical Time Warping)** | **DTW + CCA**: `L(U,V,W_x,W_y)=‖UᵀXW_x − VᵀYW_y‖²_F` | căn khi **không gian đặc trưng khác nhau** (đa thể thức/đa view) — W = căn thời gian, U,V = căn chéo modality |
- **Temporal Cycle-Consistency:** học biểu diễn bằng ràng buộc "hàng xóm gần nhất của tôi cũng coi tôi là hàng xóm gần nhất" (soft nearest neighbor + penalty), không cần nhãn.

### 2.3. Discretization / Segmentation ⭐
- Bài toán: chuỗi liên tục → nhãn rời rạc, **many-to-1** (nhiều frame → 1 phoneme).
- **CTC (Connectionist Temporal Classification, Graves 2006):** dự đoán phân phối nhãn **mỗi frame** + token **blank (∅)**; **quy tắc collapse**: gộp trùng liên tiếp → bỏ blank. Tổng xác suất trên **mọi đường** collapse về cùng chuỗi nhãn → **không cần cắt đoạn (segmentation) trước**. Blank hấp thụ khác biệt thời lượng. (Supervised.)
- **HuBERT (Hsu 2021):** **self-supervised** — clustering offline (K-means) tạo **pseudo-label (hidden units)** → mask spans → transformer dự đoán unit ở vùng bị mask. Khác CTC: target không phải phoneme mà là **cụm học từ audio không nhãn**.

---

## 3. CONTEXTUALIZED / ALIGNED REPRESENTATION — self-attention & BERT ⭐⭐⭐

**Ba lựa chọn contextualize chuỗi** (mã hóa tương tác giữa các phần tử):
| | Song song hóa | Long-range | Trọng số |
|---|---|---|---|
| **Bi-LSTM (ELMo)** | ❌ khó | qua nhiều bước | — |
| **Convolution** | ✅ được | cần **nhiều tầng** | **tĩnh** (kernel cố định) |
| **Self-attention** ⭐ | ✅ được | **trực tiếp** | **động** (attention weight) |

### 3.1. Self-Attention (Q/K/V) ⭐⭐
- Mỗi token `x_i` → **Query** `q=W_q x`, **Key** `k=W_k x`, **Value** `v=W_v x`.
- **Scaled dot-product attention:** `α_{i,j} = softmax(q_i·k_j / √d)`; output `h_i = Σ_j α_{i,j} v_j`.
- **Multi-head:** nhiều bộ `W_q,W_k,W_v` song song → attend nhiều **subspace** khác nhau → nối lại + linear projection.
- **Position embedding (bắt buộc!):** self-attention **không mã hóa vị trí** (permutation-invariant) → nếu xáo từ, output đổi chỗ tương ứng nhưng không phân biệt thứ tự. Thêm `p_i` (one-hot→linear, hoặc sinusoidal) **cộng/nối** vào `x_i`.
- **Residual connection** quanh khối attention.

### 3.2. BERT ⭐⭐ (Bidirectional Encoder Representations from Transformers)
- **Ưu điểm:** ① học đồng thời biểu diễn **token-level & sentence-level** · ② cùng kiến trúc cho pre-train & fine-tune · ③ học quan hệ **giữa 2 câu** · ④ mô hình hóa tương tác **2 chiều & long-range**.
- **Token đặc biệt:** `[CLS]` (sentence-level, `h_s`) · `[SEP]` (ngăn 2 câu). **Ba embedding cộng lại:** token + position + sentence(segment).
- **Hai mục tiêu tiền huấn luyện tự giám sát:**
  1. **Masked Language Model (MLM):** che ngẫu nhiên token → dự đoán token bị che (2 chiều).
  2. **Next Sentence Prediction (NSP):** cho 2 câu, dự đoán IsNext / NotNext (dùng **linear head trên `h_{[CLS]}`**, không dùng hidden state thô).
- **Fine-tuning 4 kiểu:** (1) phân loại câu đơn (sentiment) · (2) phân loại token (POS, slot filling) · (3) phân loại cặp câu (NLI) · (4) **QA** (học vector Start/End, argmax cho vị trí bắt đầu/kết thúc câu trả lời trong document).

### 3.3. Seq2Seq với Transformer
- **Encoder:** self-attention (nhìn cả 2 chiều). **Decoder:** **masked self-attention** (chỉ nhìn quá khứ, tránh nhìn tương lai) + **cross-attention** (Query từ decoder, Key/Value từ encoder) để nối encoder↔decoder.

---

## 4. Alignment trong FOUNDATION MODELS (2021→2026, đọc thêm)
- **CLIP (2021):** căn **sample-level global** ảnh↔caption (contrastive, chung 1 embedding space). Ma trận similarity trong batch: **đường chéo = positive**, ngoài chéo = negative; loss **đối xứng** (image→text & text→image), temperature τ. ⚠️ CLIP căn **toàn ảnh với toàn caption**, không cho **grounding vùng/token** trực tiếp — nó dạy **ranking**, không phải correspondence điểm-điểm.
- **Bridging (2022–23):** Flamingo/BLIP-2/Kosmos-2 nối vision đóng băng với LLM; grounding tường minh bắt đầu quan trọng.
- **Token/hidden-state alignment (2024–25):** **SEA** (căn visual token vào không gian LLM), **VIRAL** (regularize hidden visual state với vision foundation features → cải thiện counting/spatial reasoning). **SigLIP 2** (thêm mục tiêu phụ → grounding tốt hơn).
- **Temporal/omni (2025):** Qwen2.5-Omni đồng bộ audio+video với **TMRoPE** (time-aligned multimodal RoPE); MMAlign chỉ ra audio↔vision vẫn yếu hơn text↔vision.
- **Xu hướng:** alignment → retrieval + reranking + reasoning-aware universal embeddings (MMEB/VLM2Vec, Qwen3-VL-Embedding, PLUME latent reasoning).

---

## 🎯 CÂU HAY RA THI (Cụm D)
1. 3 sub-challenge của Alignment? Định nghĩa alignment?
2. Soft vs Hard attention: khác biệt về chọn/train/khả vi?
3. Assignment problem vs Optimal Transport: khi nào dùng cái nào? (1-1 cứng, tập bằng nhau → assignment; mềm/không đều → OT, Wasserstein).
4. 5 ràng buộc của DTW? CTW = DTW + gì?
5. CTC giải bài toán gì? Vai trò của blank token & quy tắc collapse?
6. HuBERT khác CTC ở target thế nào? (pseudo-label từ clustering, self-supervised).
7. Vì sao self-attention cần position embedding?
8. Công thức scaled dot-product attention; Q/K/V; multi-head để làm gì?
9. Hai mục tiêu pre-train của BERT? NSP dùng vector nào?
10. Encoder vs Decoder self-attention khác gì? (masked + cross-attention).
