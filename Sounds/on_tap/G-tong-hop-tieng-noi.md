# G — Tổng hợp Tiếng nói (Speech Synthesis / TTS)

> Nguồn: `06 - Speech Synthesis`. Cụm kỹ thuật: 4 thế hệ kỹ thuật, source-filter/vocoder, pipeline neural TTS, E2E, voice cloning, VALL-E, RVQ-VAE, AR vs NAR.

Điều hướng: [00-ONE-PAGER](00-ONE-PAGER.md) · [C-tiếng-Việt](C-am-vi-tieng-viet.md) · [F-đánh-giá](F-danh-gia.md) · [H-nhận-dạng](H-nhan-dang-tieng-noi.md)

---

## 1. Khái niệm & vị trí

- **Speech Synthesis (Tổng hợp tiếng nói):** quá trình **nhân tạo sinh ra tiếng nói** con người.
- **TTS (Text-To-Speech):** **một loại** speech synthesis — chuyển **văn bản → tiếng nói**.
- **Sơ đồ họ hàng (sinh tiếng nói từ nguồn khác nhau):**
  - Từ **text** → **TTS**.
  - Từ **music score** → **Singing Voice Synthesis**.
  - Từ **speech** → **Voice Conversion**.
  - (Cùng nhóm Speech Generation: Speech Enhancement…)
- **Text→Speech là ánh xạ MỘT-NHIỀU (one-to-many), multi-modal:** một câu text có thể nói theo vô số cách. Các chiều biến thiên:
  - **What to say** = nội dung (content).
  - **Who to say** = speaker/timbre (chất giọng).
  - **How to say** = prosody/emotion/style.
  - **Where to say** = background noise.
  - Text **chỉ chứa content** → phần còn lại model phải "sinh thêm".

## 2. Bốn thế hệ kỹ thuật tổng hợp — BẢNG PHẢI THUỘC

| Kỹ thuật | Ý tưởng | Ưu | Nhược |
|---|---|---|---|
| **Articulatory Synthesis** | Mô phỏng chuyển động **bộ máy cấu âm** (vocal tract) bằng mô hình toán | Cơ sở vật lý | **Phức tạp, chất lượng rất thấp**, ít kết quả |
| **Concatenative Synthesis** | **Ghép nối** các đoạn ghi âm thật (phone/syllable/word) | **Độ dễ hiểu cao (intelligibility)** | Cần **DB khổng lồ**, kém tự nhiên, **emotionless**, ít linh hoạt |
| **Statistical Parametric (SPS)** | Mô hình hoá acoustics & prosody **thống kê** (VD **HMM**), sinh "trung bình" các đoạn tương tự | **Nhẹ (small footprint), linh hoạt**, chi phí dữ liệu thấp | Chất lượng thấp hơn, **robotic** |
| **Neural End-to-End** | Mạng nơ-ron học ánh xạ text→speech | **Cải thiện chất lượng lớn**, ít tiền xử lý/feature tay | Cần dữ liệu & tính toán lớn |

- **Concatenative có 2 loại:** **Unit selection** & **Diphone synthesis**.
- **Đơn vị âm (speech unit) từ lớn → nhỏ:** Utterance (câu nói) → Prosodic Phrase (đoạn) → Word (từ) → Syllable (tiếng) → **Phoneme (âm vị — segment nhỏ nhất tri giác được)**.

## 3. Source-Filter Model (Vocoder cổ điển) — SPS/HMM

- Mô hình **nguồn–lọc (source-filter)** = hệ **tuyến tính bất biến thời gian (LTI)**:
  - **Source excitation (nguồn kích thích):** **pulse train** (âm hữu thanh) hoặc **white noise** (âm vô thanh).
  - **Vocal tract resonance (lọc):** đặc trưng bởi **state-output vector của HMM** (VD mel-cepstral coefficients, LSP coefficients).
- **HMM-based Speech Synthesis:** SPS dùng HMM sinh tham số acoustic rồi vocoder tái tạo waveform.

## 4. Pipeline Neural TTS — 3 mức "end-to-end" (HAY HỎI)

1. **Text → Text Analysis → Acoustic Model → Vocoder → Speech** (linguistic features → acoustic features → waveform) — pipeline **truyền thống/modular**.
2. **Text → Text Analysis → End-to-end TTS Model → Speech** (bỏ ranh giới acoustic/vocoder rõ ràng).
3. **Text → Fully End-to-end TTS Model → Speech** (thẳng text → waveform).

### 4.1 Ba khối chính (kiến trúc hiện đại)
- **Text Processing (NLP frontend):** Text normalization + Grapheme-to-Phoneme → linguistic features.
- **Acoustic Model:** linguistic features → **acoustic features** (thường **mel-spectrogram**).
- **Vocoder:** mel-spectrogram → **waveform** (miền thời gian).

Diễn giải encoder/decoder/vocoder:
- **Encoder:** biến text thành chuỗi vector giá trị thực, mã hoá thành hidden representation.
- **Decoder:** giải hidden representation → **acoustic features (mel-spectrogram)**.
- **Vocoder:** mel-spectrogram → **audio waveform**.

### 4.2 Text Analysis (Frontend) — biến text → linguistic features
- **Text normalization:** VD "Feb. 25th" → "February twenty fifth"; "20/1" → "hai mươi tháng một"; "ĐHBK" → "đại học bách khoa".
- **Segmentation:** phrase/word/syllable — VD "synthesis" → syn-the-sis.
- **POS tagging:** VD "I study at HUST" → [PRON, VERB, PREP, NOUN].
- **G2P (Grapheme-to-Phoneme):** VD "speech" → s p iy ch.
- Linguistic features có thể ở mức: phoneme, syllable, word, phrase, sentence.

**Đặc thù tiếng Việt (liên kết [C-tiếng-Việt](C-am-vi-tieng-viet.md)):**
- **Word segmentation:** cùng dấu cách cho **syllable và word** → nhập nhằng. VD "Học sinh học sinh học" = "Học sinh | học | sinh học" (Pupils study biology) HAY "Học sinh | học sinh | học".
- **Tonophone / PRO-SYLDIC:** allophone gắn thanh (48 phần tử → 207 tonophone).

### 4.3 Acoustic Model — chi tiết
- Dự đoán **acoustic features** từ **linguistic features**; **align** chuỗi text↔acoustic (map phoneme → biểu diễn speech liên tục). Feature: **MFCC** hoặc **mel-spectrogram**.
- Ví dụ mô hình: **Glow-TTS** — dùng **log likelihood**, prior học từ phoneme text, **alignment matrix A** thu bằng **monotonic alignment search**.

### 4.4 Vocoder — chi tiết & tiến hoá
- Biến acoustic features (spectrogram) → speech **rõ, tự nhiên**; ảnh hưởng lớn naturalness/quality/intelligibility.
- **Griffin-Lim:** cổ điển, đơn giản → **robotic**. **HiFi-GAN:** neural, chất lượng cao, real-time.
- **Tiến hoá kiến trúc:** autoregressive (**WaveNet**) → GAN-based & diffusion-based (hiệu quả hơn).
- **Thách thức vocoder:** trade-off **quality ↔ speed** (AR chậm nhưng chất lượng cao; non-AR nhanh khi inference nhưng nặng khi train); tổng quát across speaker/dataset (train 1 dataset dễ đuối với giọng lạ).

## 5. End-to-End TTS — ưu điểm

- Train bằng cặp **text-speech, tối thiểu annotation tay**.
- **Không cần alignment tường minh** giữa text↔speech.
- **Không tích luỹ lỗi / không error propagation** vì là **một model duy nhất**.
- Fully E2E: dự đoán **thẳng waveform** thay vì biểu diễn trung gian (mel).
- VD **WaveNet:** autoregressive với **dilated causal convolution**.

## 6. Voice Cloning — QUAN TRỌNG

**Định nghĩa:** tổng hợp speech **mô phỏng danh tính giọng** của một speaker cụ thể — thường từ **dữ liệu hạn chế** — cho phép nhập text tuỳ ý.

**Thách thức:** low-resource (chỉ vài phút giọng target) · speaker identity loss (mất nét riêng) · flat prosody (robotic/emotionless) · vấn đề multilingual/tonal (khó với thanh điệu tiếng Việt) · đánh giá **chủ quan, khó tự động**.

**Các loại mô hình Voice Cloning:**
- **Multi-speaker TTS + Embedding:** base Tacotron 2 / FastSpeech 2 / VITS; **speaker embedding** ghép ở encoder hoặc decoder.
- **End-to-End Voice Cloning:** text + reference audio → waveform; không có stage mel tường minh; train joint (**YourTTS, VITS2, StyleTTS2**).
- **Zero-shot Cloning:** speaker encoder pretrained (**GE2E**) + TTS backbone chung; chạy với **speaker chưa từng thấy, không cần fine-tune** (**YourTTS, SV2TTS, iSTFT-VITS, VALL-E, StyleTTS2**).

## 7. VALL-E & Neural Codec Language Model (2023) — hiện đại

- **VALL-E (Microsoft Research 2023):** **zero-shot voice cloning chỉ với prompt 3 giây**; giữ ngữ điệu/tốc độ/chất giọng gần bản gốc.
- Điểm mấu chốt: **KHÔNG sinh spectrogram** mà **dự đoán mã rời rạc RVQ (discrete codes)** rồi tái tạo.
- **Hướng cải tiến VALL-E:** prosody/style token/emotion modeling; giảm phụ thuộc prompt (robust/zero-prompt speaker embedding); multilingual/cross-lingual; dùng **semi-AR/diffusion** thay AR transformer (giảm lỗi lặp/mất đoạn); tách **content/speaker/prosody**; kết hợp **LLM** (sinh prosody token, emotion hint, chuẩn hoá text, prompt ngữ cảnh "nói giọng nghiêm túc, trầm ấm…").

### 7.1 RVQ-VAE — nền tảng của codec LM
- **VAE (Variational Autoencoder):** học phân phối ẩn (latent) để nén & tái tạo.
- **VQ-VAE:** dùng **codebook lượng tử hoá rời rạc** đại diện không gian ẩn.
- **RVQ (Residual Vector Quantization):** **nhiều tầng lượng tử kế tiếp**, mỗi tầng học **phần dư (residual)** của tầng trước → tăng biểu diễn mà **không cần codebook quá lớn**.
- **RVQ-VAE = Autoencoder + multi-stage vector quantization** → mã hoá giọng thành chuỗi mã rời rạc giàu thông tin.
- **Vai trò với TTS:** học latent speech representation (làm target train); zero-shot speaker modeling (clone từ mã ngắn); tách content↔style; **giảm gánh nặng vocoder** (chỉ cần map text → mã RVQ, không cần sinh spectrogram).

### 7.2 AR vs NAR Transformer trong TTS+RVQ — DỄ SO SÁNH
| | **AR (Autoregressive)** | **NAR (Non-Autoregressive)** |
|---|---|---|
| Cách sinh | Mỗi token dựa **toàn bộ token trước** | Sinh **cả chuỗi cùng lúc / song song theo nhóm** |
| Chất lượng prosody/intonation | **Rất tốt**, giữ nhấn nhá | Khó giữ nhịp điệu, dễ mất ngữ cảnh dài |
| Tốc độ | **Chậm** (từng token, không song song) → offline | **Nhanh hơn nhiều** → real-time |
| Vai trò | High-quality offline (VD VALL-E); **teacher** tạo ground-truth cho distillation | **Deploy online**; **student** trong distillation |

Kết hợp với RVQ giúp NAR chỉ cần sinh **mã discrete** (thay vì mel trực tiếp) → hiệu quả hơn.

## 8. Thách thức & giải pháp (đặc biệt tiếng Việt) + Tóm tắt

**Thách thức chung:** Inference speedup (giảm latency, giữ chất lượng) · Robust & Expressive TTS (intonation/rhythm/emotion đúng) · Low-resource language.

**Tiếng Việt:**
- **Word Segmentation & Text Normalization** → **hybrid models**.
- **Thiếu speech data chất lượng** → semi-/self-supervised learning + data augmentation.
- **Prosody Modeling** → style/emotion tags, style transfer / reference encoder.

**Tóm tắt tiến hoá:** Concatenative → Statistical Parametric → **Neural TTS** (ngày càng dựa **generative models**). Mainstream = **acoustic model + vocoder tách biệt**, nhưng **fully E2E đang nổi lên**. Mục tiêu chính: **tăng chất lượng, giảm chi phí**.

---

## 🎓 Mở rộng nâng cao (trình độ thạc sĩ — ngoài slide)

### N1. TTS là bài toán sinh có điều kiện (conditional generation)
- Mục tiêu: học `p(speech | text, speaker, style)` — vì one-to-many nên **phải là mô hình sinh**, không phải hồi quy điểm (regression về mel L1/L2 → ra giọng "trung bình", **over-smoothing**, mờ đục). Đây là lý do TTS hiện đại chuyển sang các họ **generative** dưới đây.
- **AR factorization:** `p(y)=Π_t p(y_t|y_{<t})`. Train **teacher forcing** → suy diễn tự hồi quy sinh **exposure bias** (lỗi tích luỹ) → skip/repeat ([G-Câu17](../trac_nghiem/G-tong-hop-tieng-noi.md)).

### N2. Bốn họ mô hình sinh — so sánh (rất hay hỏi)
| Họ | Đại diện TTS | Cơ chế | Đánh đổi |
|---|---|---|---|
| **Autoregressive** | Tacotron2, VALL-E | `Π p(y_t\|y_<t)` | Chất lượng/prosody cao, **chậm**, exposure bias |
| **Flow (chuẩn hoá)** | Glow-TTS, VITS | Biến đổi khả nghịch, **likelihood chính xác**, sinh song song | Kiến trúc ràng buộc khả nghịch |
| **VAE** | (trong VITS) | Latent + ELBO | Dễ mờ (posterior collapse) nếu không khéo |
| **Diffusion/Score** | Grad-TTS, DiffWave | Khử nhiễu nhiều bước | Chất lượng cao, train ổn định, **inference chậm** (trừ distill) |
| **GAN** | HiFi-GAN (vocoder) | Adversarial, 1 forward | **Nhanh/real-time**, train dễ bất ổn |

### N3. Bài toán alignment & duration
- **AR + attention** học alignment ngầm (dễ lỗi). **NAR** cần **duration tường minh**: **FastSpeech** dùng length regulator + duration predictor; **Glow-TTS/VITS** dùng **MAS (Monotonic Alignment Search)** — quy hoạch động tìm alignment đơn điệu tối ưu hoá likelihood, **không cần external aligner**. Đây là bước nhảy giúp NAR ổn định + nhanh.

### N4. Vocoder: bài toán khôi phục pha
- Mel-spectrogram **bỏ pha** → vocoder phải **tái tạo pha** để ra waveform. **Griffin-Lim** = lặp ước lượng pha (robotic). **Neural vocoder** học ánh xạ mel→waveform:
  - **WaveNet** (AR, dilated causal conv) — chất lượng cao, chậm.
  - **HiFi-GAN** — GAN với **Multi-Period + Multi-Scale Discriminator** bắt cấu trúc tuần hoàn (harmonic) và đa phân giải → real-time, tự nhiên.
- **Vì sao vocoder quyết định naturalness** dù mel đúng: pha & chi tiết high-freq do vocoder sinh ([G-Câu19](../trac_nghiem/G-tong-hop-tieng-noi.md)).

### N5. Neural audio codec & codec LM (VALL-E hoá bài toán TTS)
- **EnCodec/SoundStream:** nén waveform thành **token rời rạc** qua **RVQ** (nhiều tầng residual, [§7.1]). Bitrate ≈ `n_q × (f_s/hop) × log₂(codebook)` bit/s.
- **VALL-E:** coi TTS như **language modeling trên token audio** (dự đoán mã RVQ) thay vì hồi quy mel → tận dụng sức mạnh LM (in-context/zero-shot cloning từ prompt 3s). Tách **AR cho tầng RVQ đầu (prosody)** + **NAR cho tầng residual (chi tiết)**.

### N6. Điều khiển prosody & phong cách
- **GST (Global Style Tokens)** / **reference encoder:** rút style từ audio tham chiếu (unsupervised) → điều khiển biểu cảm. **VITS** hợp nhất acoustic model + vocoder + flow + VAE + adversarial thành **một E2E** (text→waveform) — kiến trúc tham chiếu hiện đại.
- **Tiếng Việt:** thanh điệu = **F0 contour mang nghĩa từ vựng** → phải mô hình hoá tường minh (tonophone/đặc trưng thanh), không để vocoder "đoán" ([G-Câu21](../trac_nghiem/G-tong-hop-tieng-noi.md)); prosody đa tầng (thanh × ngữ điệu câu) là thách thức riêng.
