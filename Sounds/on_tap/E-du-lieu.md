# E — Dữ liệu Tiếng nói (Speech Dataset)

> Nguồn: `04 - Dataset`. Cụm quy trình: xây dữ liệu, thu thập, gán nhãn, forced alignment, tiền xử lý, augmentation, benchmark/đánh giá chất lượng.

Điều hướng: [00-ONE-PAGER](00-ONE-PAGER.md) · [D-DSP](D-xu-ly-tin-hieu.md) · [F-đánh-giá](F-danh-gia.md) · [H-nhận-dạng](H-nhan-dang-tieng-noi.md)

---

## 1. Vì sao cần Speech Dataset & phân loại

Nền tảng để **huấn luyện & đánh giá** mô hình. Phục vụ: ASR, TTS, Speaker Recognition/Diarization, SER, Multimodal GenAI, MD&D…

**Các trục phân loại:**
- **Controlled vs. Spontaneous:** đọc theo kịch bản, phát âm rõ (audiobook, reading) vs. nói tự nhiên.
- **Monologue vs. Dialogue vs. Conversational:** 1 / 2 / nhiều người nói.
- **Scripted vs. Improvised:** (cho SER — nhận diện cảm xúc).
- **Clean vs. Noisy:** một số lĩnh vực không thể ghi sạch (VD air traffic control). VD dataset nhiễu-vọng: **VOiCES**.

**Dataset phổ biến theo tác vụ — NÊN NHỚ:**
| Tác vụ | Dataset |
|---|---|
| ASR | **LibriSpeech, CommonVoice, TEDLIUM, VoxPopuli** |
| Speaker Recognition & Diarization | **VoxCeleb, DIHARD, AMI Meeting, CNCeleb** |
| TTS & Synthesis | **VCTK, LibriTTS** |
| SER (cảm xúc) | **IEMOCAP, MSP-Podcast, MELD** |

## 2. Thu thập dữ liệu (Data Collection) — bảng Pros/Cons HAY RA THI

| Phương pháp | Pros | Cons |
|---|---|---|
| **Studio recording** | Chất lượng cao, sạch; điều kiện kiểm soát; dễ transcribe | Đắt, tốn thời gian; ít giống thực tế; **ít đa dạng speaker** |
| **Crowdsourced** (VD CommonVoice) | Quy mô lớn; **đa dạng speaker**; rẻ hơn studio | Chất lượng ghi âm không đều; nguy cơ nhiễu; cần QC nhiều |
| **Crawling** | Lượng dữ liệu khổng lồ; **tự nhiên, thực tế**; hợp domain-specific | Vấn đề bản quyền/pháp lý; transcription kém (cần re-annotate); chất lượng âm không đồng đều |
| **Synthesis** (dùng TTS) | **Vô hạn** dữ liệu; mô phỏng accent hiếm / low-resource | Prosody thiếu tự nhiên; có thể tạo bias; khó tổng quát ra thực tế |

**Quy trình sinh dữ liệu tổng hợp (Synthetic):** (1) Define requirements → (2) Chọn TTS model → (3) Chuẩn bị text corpus (đa dạng phoneme/câu; với tiếng Việt cần đa dạng **thanh điệu**) → (4) Generate WAV/FLAC → (5) Post-processing & Augmentation.
- **TTS model để sinh:** FastSpeech 2, Tacotron 2 + WaveGlow/WaveRNN; **VITS** (E2E, nhanh, chất lượng cao); **F5-TTS** (multi-speaker & multilingual, expressive); Neural TTS API (Azure/Google/Amazon Polly — nhanh, chất lượng cao, ít tuỳ biến).

## 3. Gán nhãn (Annotation)

- **Human annotation:** chính xác hơn nhưng cần QC quy mô lớn, **đắt**.
- **Weak labels:** thường sinh bởi **mô hình lớn hơn cùng tác vụ** (VD dùng **Whisper** tự sinh transcript làm nhãn ASR); clustering cho nhãn speaker; semi-supervised.
- **Pseudo Labeling (3 bước):** (1) train model với dữ liệu **có nhãn** → (2) dùng model dự đoán nhãn cho dữ liệu **chưa nhãn** (tạo pseudo-label) → (3) **retrain** với pseudo-labeled + labeled cùng nhau.
- **Ví dụ pipeline Vietnam-Celeb (Pham 2023):** crawl media công khai (pipeline audio-visual, gán nhãn 100% tự động/bán tự động → Speaker Recognition, SER) + ghi âm môi trường tự nhiên (crowdsource có validation/expert → MD&D, SLU).
  - **Hỗ trợ bằng visual (nhận diện speaker qua khuôn mặt):** Face detection/tracking bằng **S3FD**/**RetinaFace**; face stream ghép bounding box liên tiếp có **IoU > 0.5**; face embedding bằng **ArcFace**; loại ảnh xấu bằng **K-means**; xác minh người **đang nói thực sự** bằng **TalkNet** (Active Speaker Verification, xuất chuỗi confidence theo frame).

## 4. Forced Alignment (Căn chỉnh cưỡng bức) — QUAN TRỌNG

**Định nghĩa:** tự động **căn chỉnh audio với transcription** tương ứng (mức phoneme/word/sentence) → xác định **timestamp (start/end) chính xác** của từ/âm vị.
**Vì sao cần:** gán nhãn dataset (align transcript↔speech cho ASR/TTS) & phân tích ngữ âm/prosody (stress, intonation).

| Phương pháp | Đặc điểm | Công cụ | Hạn chế |
|---|---|---|---|
| **HMM-GMM** | Truyền thống; align phoneme vào frame xác suất cao nhất | CMU Sphinx, **Kaldi**, HTK | Kém với speech tự nhiên (mô hình phoneme cứng nhắc) |
| **Deep Learning** | DNN/CNN/Transformer; robust với giọng/nhiễu | **MFA** (Montreal Forced Aligner), Gentle | Tốn tài nguyên tính toán hơn HMM |
| **CTC-based (Hybrid)** | Dùng **CTC** tối ưu trên các path → align mềm dẻo, độ dài linh hoạt; nhanh hơn HMM | Kaldi (HMM-DNN), DeepSpeech, **Wav2Vec 2.0** | Kém chính xác hơn HMM ở **ranh giới phoneme** mịn |
| **End-to-End ASR-based** | Dùng ASR SOTA (VD **Whisper**); tốt cho speech tự nhiên/nhiễu | Aeneas, Whisper-based | Kém chính xác ở mức phoneme so với mô hình ngữ âm chuyên dụng |

## 5. Tiền xử lý dữ liệu (Data Processing)

Mục tiêu: dataset **sạch & phân đoạn tốt** → tăng độ chính xác ASR/speaker ID…
- **Speaker Diarization:** nhận & gán nhãn các người nói khác nhau ("who spoke when").
- **Speech Segmentation:** cắt ghi âm dài thành utterance (dùng **VAD**).
- **Noise Reduction:** loại nhiễu nền & reverb khi cần.
- **Volume Normalization:** chuẩn hoá mức âm.
- **Resampling:** đưa về sample rate chung (VD **16 kHz cho ASR**).
- **Silence Trimming:** cắt khoảng lặng đầu/cuối.

### 5.1 Nhiễu (Noise) trong dataset — phân loại
- **Background disturbances:** môi trường (giao thông, quạt, đám đông), microphone artifact (hiss, hum điện).
- **Transient Noise:** ngắn — click, pop, tiếng chạm mic.
- **Reverberation:** phản xạ âm khỏi bề mặt → âm kéo dài, đục (muffled).

**Kỹ thuật khử nhiễu (Noise Removal):**
- **Spectral Subtraction** — ước lượng & trừ nhiễu nền.
- **Adaptive Filtering** — VD **Wiener filter**.
- **Deep Learning Denoising** — U-Net, Denoising Autoencoder.

### 5.2 Silence Trimming
- **Silence có chủ ý** (pause giữa từ/câu) vs. **vô ý** (gap dài do lỗi ghi âm).
- **Vì sao trim:** giảm size & thời gian train; **tránh frame lặng làm bias model**; model phản hồi nhanh hơn. (VD: 7 s/660 KB → 4 s/400 KB.)
- **Kỹ thuật:** Energy-Based (loại frame biên độ rất thấp) · Thresholding (ngưỡng dB) · **VAD** (ML-based phân biệt speech/silence).

### 5.3 Speech Segmentation & VAD & Diarization
- **VAD (Voice Activity Detection):** phân biệt **speech vs non-speech**, lọc lặng & nhiễu — bằng năng lượng hoặc ML.
- **Phoneme Segmentation:** cắt tới đơn vị âm vị (cho phân tích ngữ âm & synthesis).
- **Speaker Diarization:** phân đoạn theo **danh tính người nói** — clustering đặc trưng giọng hoặc neural.

## 6. Speech Data Augmentation — HAY HỎI

- **Noise augmentation / room simulation:** thêm nhiễu nền; mô phỏng reverb bằng **RIR (Room Impulse Response)**.
- **Speed perturbation:** đổi tốc độ phát **giữ nguyên cao độ (pitch)**.
- **SpecAugment:** **masking (che)** một phần **spectrogram** (theo time/frequency).
- Công cụ: **SoX, ffmpeg** (đổi đặc tính), **RIR**, **WaveAugment, SpecAugment**.
- Ví dụ theo tác vụ: ASR (thêm noise, speed perturbation, trộn chất lượng cao/thấp) · Voice Cloning (đổi speed, pitch/intensity) · SER (đa dạng pitch/intensity/rate; nhiều speaker cùng cảm xúc để tránh **speaker bias**).

## 7. Benchmarking & Đánh giá chất lượng dataset

**4 tiêu chí then chốt: Diversity, Quality, Balance, Labeling Accuracy.**

| Nhóm | Metric |
|---|---|
| **Diversity & Representativeness** | Speaker Count & Distribution; **Phonetic Coverage**; Linguistic Coverage (phân bố tần suất từ); Environment Variety |
| **Quality & Cleanliness** | **SNR** (Signal-to-Noise Ratio, cao = tốt); **PESQ** (chất lượng theo tri giác); **STOI** (độ dễ hiểu trong nhiễu); Word/Phoneme Annotation Accuracy |
| **Balance & Bias** | Gender & Age Distribution; Accent & Language Distribution; Outlier Analysis |
| **Labeling Accuracy** | Labeling Consistency Score; Alignment Accuracy; **Inter-Annotator Agreement (IAA)** — Cohen's Kappa, Fleiss' Kappa. Xu hướng mới: **LLM as a judge** |

**Best practices:** dùng công cụ tự động (SoX, librosa, PESQ/SNR estimator; t-SNE cho speaker embedding; phân tích phân bố cho bias); chạy **benchmark model trên subset** (đo **WER, CER, EER** trước khi dùng full); **Human-in-the-Loop** verify subset; theo dõi **Dataset Drift** khi thêm dữ liệu mới.

---

## 🎓 Mở rộng nâng cao (trình độ thạc sĩ — ngoài slide)

### N1. Giả định thống kê & các loại "shift" (gốc rễ mọi lỗi tổng quát hoá)
- Học có giám sát giả định train/test **i.i.d. cùng phân phối** `P(x,y)`. Thực tế speech vi phạm:
  - **Covariate shift:** `P(x)` đổi (mic, nhiễu, kênh) — `P(y|x)` giữ.
  - **Domain/dataset shift:** đổi lĩnh vực (đọc sách → hội thoại điện thoại).
  - **Label/prior shift:** đổi phân bố lớp (SER: neutral áp đảo).
- ⇒ **Test set phải mô phỏng phân bố triển khai**; WER offline luôn **lạc quan** hơn online (nối [playbook §4](I-thuc-hanh-kinh-nghiem.md)).

### N2. Rò rỉ (leakage) & tách tập nghiêm ngặt
- **Speaker leakage** = cùng người ở train+test → đo "khớp giọng" chứ không phải generalization ([E-Câu16](../trac_nghiem/E-du-lieu.md)). Bắt buộc **speaker-disjoint**; thêm **session/device/recording-disjoint** nếu có.
- **Near-duplicate leakage:** cùng câu/đoạn crawl trùng → **dedup** (fingerprint audio + so text). **Stratify** theo giới/accent để test cân bằng.

### N3. Augmentation = mã hoá bất biến (Vicinal Risk Minimization)
- Augmentation ≈ mở rộng phân bố train quanh mỗi mẫu (**vicinal distribution**) để ép model **bất biến** với biến đổi không đổi nhãn:
  - **Noise/RIR** → bất biến kênh & phòng; **SpecAugment** → bất biến che phổ/thời gian; **speed perturbation** → bất biến tốc độ (giữ pitch).
- **Nguyên tắc:** augment phải khớp bất biến **của đúng bài toán** — speed/pitch perturb **phá** đặc trưng của **speaker verification** ([E-Câu17](../trac_nghiem/E-du-lieu.md)). Đừng augment cái mà bài toán cần phân biệt.

### N4. Bán giám sát & pseudo-label — vì sao & rủi ro
- Cơ sở lý thuyết: **cluster/manifold assumption** (dữ liệu cùng lớp tụ cụm), **consistency regularization** (đầu ra ổn định dưới nhiễu), **entropy minimization** (đẩy quyết định khỏi vùng mật độ cao).
- **Confirmation bias:** model tự củng cố lỗi của chính nó qua các vòng → giảm bằng **lọc confidence**, **teacher lớn hơn** (Whisper sinh weak label), giữ **dữ liệu nhãn thật** làm neo ([E-Câu20](../trac_nghiem/E-du-lieu.md)).

### N5. Nhiễu nhãn & đo đồng thuận (Kappa có công thức)
- **Cohen's Kappa:** `κ = (p_o − p_e)/(1 − p_e)` — `p_o` đồng thuận quan sát, `p_e` đồng thuận ngẫu nhiên kỳ vọng. κ>0.8 "gần như hoàn hảo", 0.6–0.8 "đáng kể". **Fleiss' Kappa** cho ≥3 annotator; **Krippendorff's α** cho dữ liệu thiếu/nhãn liên tục.
- **Trần hiệu năng (ceiling):** nếu người còn bất đồng (κ thấp) thì model **không thể** vượt mức nhiễu nhãn đó → sửa hướng dẫn/annotation trước khi đổ tiền vào model.

### N6. Định nghĩa metric chất lượng (hay bị hỏi bản chất)
- **SNR** `= 10·log₁₀(P_signal/P_noise)` dB (cao=sạch). **PESQ** (ITU-T P.862, ~−0.5..4.5) mô phỏng MOS chất lượng thoại. **STOI** (0..1) tương quan **độ dễ hiểu** trong nhiễu. Ba metric này đo **chất lượng/độ sạch**, khác nhóm với diversity/balance/labeling.
- **Data-centric AI:** cùng model, cải thiện **chất lượng+độ phủ dữ liệu** thường thắng tinh chỉnh kiến trúc — ưu tiên tìm & sửa **slice lỗi** (accent/số/tên riêng) hơn là tăng tham số.
