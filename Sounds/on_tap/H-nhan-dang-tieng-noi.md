# H — Nhận dạng Tiếng nói (Automatic Speech Recognition / ASR)

> Nguồn: `07 - Automatic Speech Recognition`. Cụm kỹ thuật nặng: kiến trúc AM/LM/decoder, công thức P(W|X), trích đặc trưng, HMM/Viterbi, AED/LAS, CTC, RNN-T, SSL+Transformer.

Điều hướng: [00-ONE-PAGER](00-ONE-PAGER.md) · [D-DSP](D-xu-ly-tin-hieu.md) · [E-dữ-liệu](E-du-lieu.md) · [F-đánh-giá](F-danh-gia.md)

---

## 1. Khái niệm & lịch sử

- **ASR (Automatic Speech Recognition):** nhận diện & xử lý tiếng nói con người.
- **STT (Speech-To-Text):** một loại ASR — chuyển **đoạn âm thanh lời nói → văn bản** tương ứng.
- Họ hàng: to text (**STT**), to keyword (**Keyword Spotting**), to command (**Command Recognition**).

**Lịch sử (mốc thời gian — HAY HỎI GHÉP):**
| Thời kỳ | Kỹ thuật | Đặc điểm |
|---|---|---|
| 1950s–60s | **Template Matching** | Audrey, vài chữ số, 1 người nói |
| 1970s | **Isolated Word** | DARPA, từ vựng nhỏ, feature engineering |
| 1980s | **HMM** | Pipeline modular, continuous speech, thống kê |
| 1990s | **GMM-HMM** | Dictation, speaker-independent, từ vựng lớn |
| 2000s | **Advanced ML** | Context modeling, beam search, lexicon mạnh |
| 2010s | **Deep Learning** | End-to-end (**CTC, RNN-T**), DNN-based AM |
| 2020s | **SSL + Transformers** | Pretrained (**Whisper, Wav2Vec 2.0**), multilingual, open-source |

## 2. Kiến trúc ASR truyền thống — 4 thành phần

- **Acoustic Model (AM):** tri thức về **acoustics, phonetics**, biến thiên microphone/môi trường, giới tính, phương ngữ giữa các speaker.
- **Language Model (LM):** tri thức về **từ hợp lệ**, từ nào hay đi cùng nhau & theo thứ tự nào.
- **Decoder:** sinh **chuỗi từ có xác suất hậu nghiệm (posterior) cực đại** cho vector đặc trưng đầu vào.
- **Adaptation:** chỉnh AM hoặc LM để cải thiện.

## 3. Bài toán ASR — CÔNG THỨC LÕI (Bayes)

- **Input:** chuỗi vector đặc trưng acoustic **X** (cố định).
- **Output:** chuỗi từ **W** có **P(W|X) cực đại**.

```
Ŵ = argmax_W P(W|X) = argmax_W P(X|W) · P(W)
                                 └ AM ┘   └ LM ┘
```
- **P(W)** = **Language Model** — độ phức tạp từ vựng/ngữ pháp & biến thiên ngôn ngữ nói.
- **P(X|W)** = **Acoustic Modeling ~ Phonetic Modeling** — biến thiên speaker, phát âm, môi trường, **coarticulation phụ thuộc ngữ cảnh**.
- **LMSF (Language Model Scaling Factor) λ₁:** hệ số hiệu chỉnh trade-off giữa acoustic & chuỗi từ phổ biến — vì AM **đánh giá thấp P(X|W)** do **giả định độc lập (independence assumption)** trên xác suất phone.
- LM: model truyền thống ngầm học LM cho ký tự từ dữ liệu train, nhưng transcript có thể **không đủ text** để có LM tốt → **ghép LM lớn ngoài** để cải thiện.

## 4. Trích đặc trưng: Windowing → Mel filter bank (liên kết [D-DSP](D-xu-ly-tin-hieu.md))

- **Windowing:** chia tín hiệu thành **frame** ngắn để tính chất thống kê **coi như ổn định** trong frame → trích feature mỗi frame. VD **cửa sổ 25 ms, stride 10 ms** (frame size, stride, shape).
- **Giảm spectral leakage:** dùng **Hamming window** — co giá trị tín hiệu về 0 ở biên cửa sổ, tránh **gián đoạn (discontinuity)** so với **Rectangular**.
- **Mel scale:** đơn vị cao độ, thang tần số thính giác cho tai người.
- **Mel filter bank:** bank các bộ lọc thu năng lượng từng dải tần, **giãn logarit** — **phân giải rất mịn ở tần thấp, thô ở tần cao** (tai người **kém nhạy ở tần cao**). Sau đó lấy **log**.

## 5. Các kỹ thuật ASR — tiến hoá: HMM → AED → CTC → RNN-T → SSL+Transformer

### 5.1 HMM-based ASR
- Biên dịch tác vụ nhận dạng (finite grammar) thành **composite HMM**.
- Giải mã bằng **thuật toán Viterbi** (tìm đường trạng thái xác suất cao nhất). Nền tảng cho GMM-HMM.

### 5.2 Attention-based Encoder-Decoder (AED) — LAS
- **LAS (Listen, Attend and Spell):** encoder-decoder + **attention**; loss = **cross-entropy** (xác suất output khớp label).
- **Hai vấn đề đặc thù ASR mà AED giải:**
  - **Length differences:** chuỗi acoustic **rất dài** (VD 200 frame 10 ms) → chuỗi ký tự **ngắn** (VD 5 chữ) ⇒ AED có **compression stage** rút ngắn chuỗi + **attention** tập trung phần input khác nhau.
  - **Input-output mapping:** khó biết phần nào của X ↔ phần nào của Y ⇒ attention **align** không cần cấu trúc định trước.
- **Nhược AED:** attention **đắt** cho chuỗi dài (**O(mn)**, m,n lớn với audio); **không chạy online/real-time** (cần toàn bộ input trước khi decode); **không tận dụng tính đơn điệu (monotonic)** của alignment speech (từ A sau B trong transcript ⇒ A sau B trong audio) → thiếu inductive bias này khiến **khó train**, thường phải thêm auxiliary loss.

### 5.3 CTC (Connectionist Temporal Classification)
- Dự đoán chuỗi ký tự **không cần khớp độ dài input/output** → xử lý output độ dài thay đổi, học được từ hiếm.
- **Thuật toán:** xuất **1 ký tự mỗi frame** (output cùng độ dài input) → áp **collapsing function** gộp chuỗi ký tự giống nhau liên tiếp → chuỗi ngắn hơn.
- **Blank token:** thêm ký hiệu **blank** vào bảng chữ để biểu diễn khoảng trống giữa từ/phần từ & phân tách ký tự lặp thật.
- **Loss:** tổng xác suất **mọi alignment khả dĩ** ra output đúng, **không cần align chính xác** input↔output.
- **Inference:** encoder-only, decode bằng **softmax đơn giản** trên vocab ký tự mỗi time step (~sequence modeling).
- **Hai vấn đề của CTC:**
  - **Problem 1:** độ dài output **phải nhỏ hơn** độ dài input → cản việc pooling nhiều (làm model nhanh hơn).
  - **Problem 2:** **giả định các output độc lập nhau** → hay ra output sai kiểu "I eight food" thay vì "I ate food"; cần **search + LM phụ**.
- Có thể **kết hợp CTC + Encoder-Decoder** (cộng CTC loss với cross-entropy loss).

### 5.4 RNN-T (Transducer) — HAY HỎI, HỢP STREAMING
- **RNN-T:** mô hình **seq2seq end-to-end**, **học alignment audio↔text** mà **không cần align frame-level tường minh**; hỗ trợ **streaming ASR** (sinh transcript khi audio đang tới).
- **Giải cả 2 vấn đề của CTC:**
  - Problem 1 → cho phép **nhiều output cho mỗi input**.
  - Problem 2 → thêm **Predictor network** + **Joiner network**.
- **Cấu trúc:**
  - **Encoder:** sinh vector acoustic **fₜ** từ audio.
  - **Predictor (autoregressive):** nhận **output trước đó**, sinh **gᵤ** — như một **language model**.
  - **Joiner:** feedforward, kết hợp fₜ & gᵤ → **softmax hₜ,ᵤ** trên nhãn + output **null ∅**.
- **Vì sao hợp streaming:** xử lý **frame-by-frame** không cần cả câu; **không cần forced alignment**; **incremental output** (emit từ khi audio đang tới); **monotonic decoding** (khớp trái→phải của lời nói); **context-aware** nhờ predictor giữ output trước (CTC không có decoder nên thiếu ngữ cảnh); **Joint network** kết hợp acoustic + linguistic để quyết định emit.
- **Nhược RNN-T:** latency, độ chính xác với **ngữ cảnh dài**, **train đắt**.
- **Cải thiện RNN-T:** thay RNN bằng **Transformer/Conformer**; thay Predictor bằng Transformer nhẹ; thêm CTC/LM/alignment-aware loss; ghép **external LM**; multilingual & code-switching.
- **ILM vs External LM:** RNN-T model **trực tiếp P(W|X)** (khác AM truyền thống model likelihood **P(X|W)**). LMSF λ₁, λ₂ hiệu chỉnh trade-off; **trừ nhiều ILM ⇒ cần cộng thêm nhiều external LM** để bù.

### 5.5 CTC vs RNN-T — SO SÁNH NHANH
| | **CTC** | **RNN-T** |
|---|---|---|
| Decoder/ngữ cảnh | **Không** decoder → output **độc lập**, thiếu ngữ cảnh | Có **Predictor** (autoregressive) → context-aware |
| Streaming | Thường **đợi** cả chunk/utterance rồi collapse | **Token-by-token**, streaming-friendly |
| Alignment | Học tự động, monotonic | Học tự động, monotonic, linh hoạt (nhiều output/input) |
| Cần LM ngoài | Thường cần LM phụ để đúng | Có internal LM (predictor), vẫn dùng LMSF |

### 5.6 SSL + Transformer (2020s) — SOTA
- **SSL (Self-Supervised Learning):** pretrain trên **lượng lớn audio KHÔNG nhãn** → học biểu diễn tốt; train bằng cách **dự đoán phần bị mask** (masking-based) hoặc task tự định nghĩa; biểu diễn nắm **thông tin acoustic/phonetic tổng quát**.
- **Transformer:** **self-attention** mô hình quan hệ giữa các phần chuỗi; nắm **phụ thuộc xa** tốt hơn RNN; **xử lý song song** → train nhanh.
- **Vì sao kết hợp:** học từ audio không nhãn (pretrain quy mô lớn); tổng quát tốt (robust across speaker/accent/domain); **low-resource friendly** (ít fine-tune vẫn tốt); **multilingual & zero-shot** (Whisper, HuBERT).
- **APC (Autoregressive Predictive Coding, Chung 2019):** dự đoán feature spectral (log-Mel/MFCC) **~50 ms tương lai** từ quan sát hiện tại & quá khứ.
- **Model SSL+Transformer phổ biến — bảng đa ngôn ngữ:**
  | Model | Multilingual? | Ghi chú |
  |---|---|---|
  | **Wav2vec 2.0** | Gốc monolingual | Train English (LibriSpeech), fine-tune sang ngôn ngữ khác |
  | **HuBERT** | Monolingual | Chủ yếu English, adapt được |
  | **WavLM** | Chủ yếu English | Tổng quát tốt khi fine-tune |
  | **Whisper** | **Yes** | Train **680k giờ, 96+ ngôn ngữ** — ASR + translation **out-of-the-box** |
  | **Data2vec** | Speech version monolingual | Cross-modality SSL |
  | **XLSR** (cross-lingual Wav2vec 2.0) | **Yes** | Train **53+ ngôn ngữ** (CommonVoice, BABEL) |
- **XLSR-Transducer (2024):** streaming ASR cho SSL pretrained models.

## 6. Thách thức & giải pháp ASR

**Thách thức:** Accuracy of Recognition (khó với ngữ cảnh phức/nói không rõ); Language Complexity (đa dạng accent/variation); Context Understanding (nghĩa sâu). Cụ thể: **rare words / specialized terms** & **proper names** (tên riêng, địa danh, công ty).

**Giải pháp:** Deep Learning (Transformer & biến thể); Optimized/diverse training data; tích hợp **ML + NLP**; **context-awareness**; với rare word/proper name → **expand training data**, **transfer learning**, tích hợp **NER (Named Entity Recognition)**, tối ưu model/algorithm.

**Xu hướng ASR:** Self-supervised Learning · Multi-language ASR · Robustness & Adaptability · Context-aware · Personalized ASR · tích hợp AI & NLP.

---

## 🎓 Mở rộng nâng cao (trình độ thạc sĩ — ngoài slide)

### N1. Noisy channel & vì sao có LM
- ASR = **kênh nhiễu**: người nói phát `W`, kênh (âm học + thu) biến thành `X`; ta khôi phục `Ŵ = argmax P(W|X)`. Bayes: `P(W|X) ∝ P(X|W)·P(W)` (bỏ `P(X)` vì cố định).
- **LMSF** giải bất đối xứng thực nghiệm: `score = log P(X|W) + λ·log P(W) + η·|W|` (thêm **word insertion penalty** η). AM đánh giá thấp `P(X|W)` do **giả định độc lập frame/phone** → cần λ cân lại.

### N2. GMM-HMM: sinh mô hình, EM, Viterbi
- **HMM** cho mỗi phone (thường 3 state trái→phải): tham số = xác suất **chuyển** `a_{ij}` + **phát xạ** `b_j(x)` (GMM). Triphone để bắt **coarticolation phụ thuộc ngữ cảnh** ([B §N5](B-ngu-am-hoc.md)); state tying (senones) để giảm tham số.
- **Train = Baum–Welch (EM):** forward–backward tính posterior chiếm state γ, cập nhật a,b (không cần alignment tay). **Forced alignment** = Viterbi với transcript đã biết.
- **Decode = Viterbi:** quy hoạch động tìm đường state khả dĩ nhất `δ_t(j)=max_i δ_{t-1}(i)a_{ij}b_j(x_t)`, `O(T·S²)`.
- **WFST decoding:** hợp thành `HCLG = H∘C∘L∘G` (HMM ∘ context ∘ lexicon ∘ grammar) thành một đồ thị giải mã tối ưu — kiến trúc Kaldi.

### N3. CTC — toán học
- Đặt path `π` (dài T trên vocab + blank); `B` = collapse (bỏ lặp rồi bỏ blank). Xác suất chuỗi `y`:
```
P(y|X) = Σ_{π ∈ B⁻¹(y)} Π_t P(π_t | X_t)     (giả định độc lập theo frame)
Loss  = − log P(y|X)   ← tính bằng forward–backward động (O(T·|y|))
```
- **Giả định độc lập frame** (Problem 2) ⇒ CTC có **internal LM yếu** → cần LM ngoài. **Peaky behavior:** posterior dồn vào vài frame, phần lớn ra blank.

### N4. RNN-T — lattice T×U
- Sinh trên **lưới 2 chiều** `(t, u)`: mỗi ô Joiner(f_t, g_u) cho phân phối trên (nhãn ∪ ∅); ∅ = "tiến thời gian", nhãn = "tiến token". Loss = `−log Σ` mọi đường từ (0,0)→(T,U) (forward–backward 2D).
- **Chi phí:** activation tensor `T×U×V` rất lớn ⇒ khó train (function-merging, gradient checkpointing). Predictor = **internal LM** (autoregressive) → context-aware, hợp streaming.

### N5. AED/LAS & bẫy huấn luyện
- Factorization `P(y|X)=Π_u P(y_u|y_{<u},X)`, attention align. **Exposure bias** (train teacher-forcing, infer tự do) → dùng **scheduled sampling**; **label smoothing** chống overconfident; thường **hybrid CTC/attention** (đa nhiệm, CTC ép monotonic giúp attention hội tụ).

### N6. SSL — mục tiêu tự giám sát khác nhau (rất hay hỏi so sánh)
| Model | Tín hiệu học | Cơ chế |
|---|---|---|
| **wav2vec 2.0** | Contrastive | Che latent, phân biệt quantized target thật với distractor + **diversity loss** giữ codebook đa dạng |
| **HuBERT** | Masked prediction | Dự đoán **nhãn cụm k-means** (target rời rạc, lặp lại tinh dần) ở vị trí bị che |
| **WavLM** | Masked + denoising | HuBERT + trộn nhiễu/overlap → mạnh cho speaker/diarization |
| **Whisper** | **Weakly-supervised** | 680k giờ (audio, text) web — không phải SSL thuần; robust & multilingual out-of-the-box |
- Tinh thần chung: dùng **audio KHÔNG nhãn** học biểu diễn âm học/ngữ âm tổng quát → fine-tune với ít nhãn (low-resource friendly).

### N7. Conformer & LM fusion
- **Conformer** = Macaron FFN + **Self-attention (toàn cục)** + **Convolution (cục bộ)** → SOTA AM streaming/offline.
- **Ghép LM:** **Shallow fusion** (cộng log P_LM lúc beam search) · **Deep/Cold fusion** (hợp nhất trạng thái LM khi train) · **Density-ratio / ILME** (trừ **internal LM** ước lượng của E2E rồi cộng external LM đúng cách) — quan trọng khi đổi domain.
- **Decode & streaming:** **beam search** (giữ k giả thuyết) > greedy; **endpointing** quyết định lúc dừng; **lookahead/chunk** đánh đổi **latency ↔ WER** ([H-Câu23](../trac_nghiem/H-nhan-dang-tieng-noi.md)).
