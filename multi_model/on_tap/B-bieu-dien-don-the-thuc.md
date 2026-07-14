# CHEAT-SHEET — Cụm B: Biểu diễn Đơn thể thức (Unimodal Representations)
Nguồn: `lecture2.1-UnimodalRepresentations-Part1` (thị giác/CNN), `Lecture2_2_unimodal_path2` (ngôn ngữ, RNN/LSTM/GRU, seq2seq, syntax). Đây là nền tảng *encoder* cho từng modality trước khi ghép đa thể thức.

---

## 1. Nguyên tắc chung: pixel ≠ semantics ⭐

- **Vấn đề cốt lõi:** khoảng cách pixel **≠** khoảng cách ngữ nghĩa. Cùng một nhãn `y` nhưng pixel thay đổi lớn (ánh sáng, scale, nền); ngược lại vật khác nhau có thể có vector pixel giống nhau.
- **Ba cách tạo bất biến (invariance):**
  1. **Data augmentation** (crop, flip, color jitter, rotation) — buộc model coi các biến thể là cùng nhãn.
  2. **Convolution + Pooling** — conv = weight sharing cục bộ; pooling = bất biến dịch chuyển cục bộ (by design).
  3. **Attention** — tập trung phần liên quan bất kể vị trí; self-attention **permutation-equivariant**.
- **Equivariance vs Invariance ⭐:** conv **equivariant** (input dịch → feature map dịch theo); pooling/GAP tạo **invariance** (đại diện gần như không đổi khi dịch nhỏ).

---

## 2. Biểu diễn theo từng MODALITY (bảng profile) ⭐⭐

| Modality | Element | Structure | Bất biến điển hình | Model điển hình |
|---|---|---|---|---|
| **Image** | pixel/patch (liên tục) | lưới 2D không gian | dịch chuyển, scale | CNN, ViT |
| **Text** | token/subword (rời rạc) | chuỗi 1D (Zipfian, thưa) | context nhạy | RNN, Transformer |
| **Audio** | sample/frame (liên tục) | time hoặc F×T | dịch thời gian nhỏ | CNN, Conformer |
| **Table** | numeric + categorical | rows/columns (schema) | hoán vị hàng | MLP, GBDT, TabTransformer |
| **Graph** | node + edge | topology quan hệ | **hoán vị node** | GNN, graph transformer |
| **Set** | phần tử vô thứ tự | không có thứ tự cố định | **permutation invariance** | DeepSets, Set Transformer |

- **Modality profile** = so sánh modality trên 6 trục heterogeneity (element rep, distribution, structure, information, noise, relevance) → quyết định preprocessing + inductive bias + kiến trúc.
- **DeepSets** (bất biến hoán vị): `f(S) = ρ(Σᵢ φ(xᵢ))` — φ mã hóa từng phần tử, pooling (sum/mean) bất biến thứ tự, ρ dự đoán.
- **Graph message passing:** `h_v^{k+1} = Update(h_v^k, Aggregate({h_u^k : u∈N(v)}))`; hoán vị node: `A' = P A Pᵀ` (nghĩa không đổi).

---

## 3. THỊ GIÁC: từ đặc trưng thủ công đến CNN

- **Inductive bias cho vision:** locality · translation equivariance · hierarchical composition (edges → parts → objects).
- **Đặc trưng thủ công (hand-crafted):** image gradient, edge detection, **HOG** (histogram of oriented gradients: gradient → bin hướng → histogram theo cell → block normalization), **Gabor filters** (lấy cảm hứng vỏ não thị giác V1, chọn lọc hướng × tần số). → CNN layer 1 **tự học lại** filter kiểu Gabor.
- **Object-based representation:** detector + attribute classifier. Tốt cho VQA/retrieval/captioning/interpretability; **hỏng** khi detection sai, bỏ sót vật nhỏ/bị che, thiếu layout/context.

### 3.1. Convolution — công thức phải nhớ ⭐
- `y[i,j] = Σ_u Σ_v K[u,v]·X[i+u, j+v]` (tích chập = dot của patch với kernel).
- **Kích thước output:** `H_out = ⌊(H + 2P − D(K−1) − 1)/S + 1⌋` (P=padding, S=stride, D=dilation, K=kernel).
- **Đếm tham số:** FC = `(H·W·C)·K + K`; Conv = `(k_h·k_w·C_in)·F + F`. → Conv = **linear map với ma trận thưa, chia sẻ trọng số** ⇒ ít tham số hơn MLP nhiều, translation-equivariant.
- **Multi-channel:** 1 filter phủ toàn bộ `C_in`; F filter → `C_out = F`.
- **Pooling:** max (giữ activation mạnh nhất) / avg (mượt) / strided conv (downsample học được).
- **GAP (Global Average Pooling):** trung bình mỗi feature map → 1 scalar; ít tham số + làm **CAM** dễ (class score = tổng có trọng số các feature map).

### 3.2. Kiến trúc CNN (timeline) & ResNet
- LeNet(1998) → AlexNet(2012: ReLU+dropout+GPU) → VGG(2014: stack 3×3) → Inception(2014: multi-scale) → **ResNet(2015: skip)** → ConvNeXt(2022).
- **ResNet residual block:** `y = F(x) + x`. Đường skip identity giúp **gradient chảy tốt** → train mạng rất sâu (tới 152 tầng).
- **Transfer learning recipe:** freeze backbone → train head → gradually unfreeze → fine-tune LR thấp.

### 3.3. Object detection & giải thích
- **Metrics:** IoU (overlap/union), confidence = objectness × class prob, **NMS** (giữ box điểm cao, khử box chồng lấn), **mAP** (diện tích dưới precision-recall, trung bình các lớp/ngưỡng IoU).
- **Two-stage (Faster R-CNN, RPN)** = chính xác hơn/chậm hơn · **One-stage (YOLO/SSD)** = nhanh, real-time · **DETR** = transformer set prediction, end-to-end matching.
- **Visualize:** t-SNE (local cluster tốt, O(n²), distance toàn cục không tin được) vs **UMAP** (nhanh 4–10×, global structure tốt hơn, reproducible). **CAM** (cần GAP+linear) vs **Grad-CAM** (kiến trúc bất kỳ, dùng gradient; `α_k^c = GAP(∂y^c/∂A^k)`, `L = ReLU(Σ α_k^c A^k)`). **Sanity check (Adebayo 2018):** giải thích tốt phải **thay đổi mạnh** khi randomize trọng số — nếu không, nó chỉ phản ánh ảnh chứ không phải model.

---

## 4. NGÔN NGỮ: từ one-hot đến embedding

- **Pipeline:** Text → Tokenize (BPE/WordPiece/SentencePiece) → Token IDs → One-hot (thưa, dim=|V|) → **Embedding lookup** (dense, ℝ^d, d≈768) → ma trận T×d.
- **Subword tokenization** giải quyết OOV: "unhappiness" → [un, happi, ness]; giảm vocab, xử lý từ hiếm/morphology/typo.
- **Distributional hypothesis ⭐:** nghĩa của từ ≈ các từ xung quanh nó ("bardiwac" đoán được là rượu vang đỏ qua ngữ cảnh). Similarity = gần nhau trong không gian (cosine/góc quan trọng hơn độ dài).

### 4.1. Word2Vec / GloVe / fastText ⭐⭐
| | Cách tiếp cận | Ý chính | Hạn chế |
|---|---|---|---|
| **Word2Vec** (2013) | prediction, cửa sổ cục bộ | **Skip-gram** (center→context) / **CBOW** (context→center) | 1 vector/từ, không polysemy, không subword |
| **GloVe** (2014) | count, ma trận toàn cục | factorize `log X_ij` (weighted least squares) | tốn bộ nhớ ma trận đồng xuất hiện |
| **fastText** (2017) | prediction + subword n-gram | `v_word = v_whole + Σ v_ngram` | vẫn static, model lớn hơn |

- **Skip-gram vs CBOW:** Skip-gram (1 center → nhiều context, tín hiệu nhiều hơn, tốt cho từ hiếm) · CBOW (trung bình context → center, nhanh hơn).
- **Negative sampling ⭐:** thay full softmax `O(V)` (100K dot products) bằng 1 positive + K negative (`O(K)`, K=5–15) → **binary classification real-vs-noise**. Objective: `max log σ(v'_pos·v) + Σ_k log σ(−v'_neg,k·v)`. Sampling `P(w) ∝ freq(w)^{3/4}` (nâng từ hiếm, tránh 'the' áp đảo).
- **GloVe ≈ Word2Vec:** Levy & Goldberg (2014) — skip-gram+negative sampling **ngầm factorize ma trận shifted PMI**; GloVe làm điều đó tường minh. → cho không gian gần giống nhau.
- **Tính chất nổi lên:** `vec(king) − vec(man) + vec(woman) ≈ vec(queen)`; nhưng **có social bias** (`programmer − man + woman ≈ homemaker`).
- **Hạn chế static:** một vector cho mọi nghĩa ("bank" tài chính vs bờ sông) → **contextual embeddings (ELMo biLSTM, BERT Transformer)** cho mỗi token một vector riêng.

---

## 5. MÔ HÌNH CHUỖI: RNN → LSTM/GRU → Attention

- **Bag-of-words hỏng với thứ tự:** "dog bites man" = "man bites dog" nếu trung bình embedding → cần model tôn trọng thứ tự.
- **RNN vanilla:** `h(t) = tanh(U·x(t) + W·h(t−1))`, `z(t)=matmul(h(t),V)`, chia sẻ tham số qua mọi bước thời gian. Sequence label → chỉ dùng `h(N)`.
- **BPTT & vanishing gradient ⭐:** gradient bước 1 = `∏ ∂h(t)/∂h(t−1)`; mỗi factor <1 → **triệt tiêu** theo hàm mũ (0.6¹⁰≈0.006); >1 → **bùng nổ**.

### 5.1. LSTM ⭐⭐ (phải thuộc)
- **3 cổng + cell state:**
  - Forget: `f_t = σ(W_f[h_{t−1},x_t]+b_f)` — xóa gì.
  - Input: `i_t = σ(...)`, candidate `c̃_t = tanh(...)` — viết gì.
  - Cell update: `c_t = f_t ⊙ c_{t−1} + i_t ⊙ c̃_t`.
  - Output: `o_t = σ(...)`, `h_t = o_t ⊙ tanh(c_t)`.
- **Vì sao fix vanishing:** `∂c(t)/∂c(t−1) = f_t` (chỉ là forget gate!) — không nhân ma trận, không squash tanh; `f_t ≈ 1` → **"gradient highway"** cho thông tin chảy xa.

### 5.2. GRU (gọn hơn)
- **2 cổng, 1 state:** reset `r_t`, update `z_t`, candidate `ĥ_t = tanh(W·x_t + U·(r_t⊙h_{t−1}))`, `h_t = (1−z_t)⊙h_{t−1} + z_t⊙ĥ_t`.
- **z_t = 0** → copy state cũ (giải vanishing). GRU: ~25% ít tham số hơn LSTM, hiệu năng tương đương. **Mẹo nhớ:** LSTM nhớ bằng `f_t≈1`; GRU nhớ bằng `z_t≈0` (ngược convention, cùng hiệu ứng).

### 5.3. Seq2seq + Attention ⭐
- **Encoder-decoder** nén cả câu nguồn thành 1 context vector → nghẽn.
- **Attention (Bahdanau):** mỗi bước decoder tính context mới `c_t = Σ α_i h_i`; trọng số α cho biết từ nguồn nào quan trọng lúc này → cải thiện câu dài + lộ **alignment** (heatmap gần đường chéo cho cặp ngôn ngữ cùng thứ tự). Không cần giám sát alignment.
- **Decoding:** greedy (chọn tốt nhất cục bộ) vs **beam search** (giữ top-B giả thuyết) — train = cross-entropy token; inference = **search trên cả chuỗi**.
- **Teacher forcing:** train feed gold token trước → nhanh nhưng gây **exposure bias** lúc test.

### 5.4. Perplexity ⭐
- `L = −(1/N) Σ_t log p(w_t|w_{<t})`, **`PPL = exp(L)`**. PPL=10 ≈ mơ hồ như chọn giữa 10 từ đồng khả năng. Chỉ so sánh khi cùng tokenization/vocab.

---

## 6. CẤU TRÚC CÚ PHÁP & TreeRNN
- **Phrase-structure (constituency)** parse tree vs **dependency grammar** (subject/object/attribute). Ngôn ngữ **phân cấp**, không chỉ tuần tự.
- **Recursive NN / TreeRNN:** kết hợp cặp `[x1;x2]` theo cây parse: `p = tanh(W[x1;x2])`. **Tree-LSTM:** `c_p = f_l⊙c_l + f_r⊙c_r + i⊙c̃_p` — forget gate riêng cho mỗi con; gradient path ngắn hơn RNN tuần tự ("man" ghép trực tiếp với "boats").
- **Ambiguity:** POS đa nghĩa ("like"=verb/preposition), gắn kết cấu trúc mơ hồ ("salesmen sold the dog biscuits").

---

## 🎯 CÂU HAY RA THI (Cụm B)
1. Vì sao pixel distance ≠ semantic similarity? 3 cách tạo invariance?
2. Công thức output size của conv; đếm tham số conv vs FC.
3. Equivariance vs invariance khác nhau chỗ nào (conv vs pooling)?
4. Skip-gram vs CBOW; negative sampling giải quyết gì và tại sao `^{3/4}`?
5. Vì sao LSTM giải vanishing gradient? (`∂c_t/∂c_{t−1}=f_t`).
6. LSTM vs GRU: số cổng, số state, cách "nhớ".
7. Attention giải bottleneck gì của seq2seq? Perplexity = ?
8. DeepSets/GNN đảm bảo bất biến gì? Static vs contextual embedding.
