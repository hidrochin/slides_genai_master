# ONE-PAGER — Ôn nước rút Tạo sinh Âm thanh (liếc trước giờ thi)

Tổng hợp & Nhận dạng Tiếng nói. Chi tiết ở: [A-tổng-quan](A-tong-quan.md) · [B-ngữ-âm-học](B-ngu-am-hoc.md) · [C-tiếng-Việt](C-am-vi-tieng-viet.md) · [D-DSP](D-xu-ly-tin-hieu.md) · [E-dữ-liệu](E-du-lieu.md) · [F-đánh-giá](F-danh-gia.md) · [G-tổng-hợp](G-tong-hop-tieng-noi.md) · [H-nhận-dạng](H-nhan-dang-tieng-noi.md)

---

## 🔢 CÔNG THỨC PHẢI NHỚ

| Chủ đề | Công thức | Ghi nhớ |
|---|---|---|
| **Bit rate** | `Bit rate = Bit depth × Sample rate × Channels` | bit/giây |
| **File size** | `Size = Bit rate × Duration` = `Sample rate × Bit depth × Channels × Dur` | ÷8 để ra byte |
| **Bit depth → mức** | `Số mức = 2^(bit)`; ngược: `bit = log₂(mức)` | 16 bit → 65 536 mức |
| **Nyquist** | `Sample rate ≥ 2 × f_max` | Nyquist freq = ½ sample rate; vi phạm → **aliasing** |
| **F0** | `F0 = số chu kỳ / thời gian` | 10 chu kỳ / 0.03875 s = 258 Hz; harmonic n = n×F0 |
| **WER** | `WER = (S + D + I) / N` | N = số từ **reference**; `WAcc = 1 − WER` |
| **RTF** | `RTF = t_tổng_hợp / thời_lượng_audio` | **RTF < 1** = nhanh hơn real-time |
| **EER** | Điểm mà `FAR = FRR` | **EER thấp = tốt**; verification 1-1 |
| **ASR (Bayes)** | `Ŵ = argmax P(X\|W)·P(W)` | P(X\|W)=**AM**, P(W)=**LM** |
| **CD quality** | 44.1 kHz / 16 bit / stereo = **1 411 kbps** | ≈10.584 MB/phút |

---

## ⚖️ SO SÁNH LÕI (dễ bị lừa)

**Phonology vs Phonetics:** Phonology = hệ âm **một ngôn ngữ**, trừu tượng, **language-specific**. Phonetics = **vật lý** của âm, **universal**. 3 nhánh Phonetics: **Articulatory** (tạo ra) · **Acoustic** (vật lý) · **Auditory** (tri giác).

**Grapheme vs Phoneme:** Grapheme = đơn vị **viết** nhỏ nhất. Phoneme = đơn vị **âm** nhỏ nhất. **Allophone** = biến thể phoneme (không đổi nghĩa, theo ngữ cảnh) — ký hiệu `[ ]` vs `/ /`.

**Phụ âm 3 chiều:** **Place** (Labial/Coronal/Dorsal) · **Manner** (Stop/Nasal/Fricative/Approximant/Lateral) · **Voicing** (voiced rung dây thanh vs unvoiced không rung). Nhớ cặp: b/p, d/t, z/s, v/f.

**Nguyên âm 2 chiều:** **Height** (High/Mid/Low) · **Backness** (Front/Central/Back).

**Sample rate vs Bit depth vs Bit rate:** lần lấy mẫu/giây · số bit/mẫu (mức biên độ) · số bit/giây. Đừng quên **× số kênh** khi tính size.

**Lossy vs Lossless:** MP3/AAC/OGG/Opus (mất vĩnh viễn, 70–90% nhỏ) · FLAC/ALAC (nguyên gốc, 30–70% nhỏ) · WAV/AIFF (uncompressed).

**Spectrogram:** Spectrum + Time. **Nguyên âm** có formant (F1,F2); **phụ âm** không formant riêng, chỉ ảnh hưởng nguyên âm quanh nó.

**Mel spectrogram vs MFCC:** cùng khớp thang **Mel** (tri giác người); Mel-spec giữ trục Mel, **không giữ raw frequency**; MFCC = nén power spectrum (qua cepstrum) thành ít hệ số.

**Họ MOS:** **MOS** (tốt cỡ nào, 1–5) · **DMOS** (xuống cấp cỡ nào) · **CMOS** (A/B cái nào hơn, −3..+3) · **SMOS** (giống style/speaker không).

**Objective vs Subjective (TTS):** Objective = MCD, RTF, Speaker Similarity (cosine↑/euclid↓). Subjective = MOS/CMOS/SMOS, ABX/AB.

**Speaker Verification vs Identification:** Verification **1-1** (đúng người claim?) → **EER (FAR=FRR)**. Identification **1-N** (là ai?) → **Accuracy / Top-k**.

**CTC vs RNN-T:** CTC không decoder → output **độc lập**, thường đợi cả chunk; giả định output độc lập; output ngắn hơn input. RNN-T có **Predictor + Joiner** → context-aware, **streaming token-by-token**, giải cả 2 vấn đề CTC.

**AED/attention vs CTC vs RNN-T:** AED attention **O(mn)**, không online, thiếu monotonic bias. CTC monotonic nhưng độc lập. RNN-T monotonic + có ngữ cảnh + streaming.

**AR vs NAR (TTS+RVQ):** AR chậm, chất lượng/prosody cao, offline, teacher. NAR nhanh/song song, real-time, student, khó giữ intonation.

**4 thế hệ TTS:** Articulatory (mô phỏng cấu âm, chất lượng thấp) → Concatenative (ghép âm thật, intelligible nhưng cần DB lớn, emotionless) → Statistical Parametric/HMM (nhẹ/linh hoạt, robotic) → **Neural E2E** (chất lượng cao).

---

## 🧮 CÔNG THỨC/QUY TRÌNH TIẾNG VIỆT

**Cấu trúc âm tiết:** `(C1)(w)V(C2)-T` — âm đầu, âm đệm /w/, âm chính (bắt buộc), âm cuối, thanh. VD **chuyển** [tɕwiən-3].
**Thanh Hà Nội:** **6 thanh** với âm cuối sonorant, **2 thanh** (sắc/nặng) với âm cuối obstruent /p t k/ (ngắn: 5b, 6b).
**Âm đệm /w/:** viết "o" trước nguyên âm rộng (a,ă,e); "u" trước (y,ê,ơ,â).
**Tonophone:** allophone + thanh (gắn thanh vào rhyme, không gắn âm đầu) → **48 phần tử → 207 tonophone** (PRO-SYLDIC).

---

## 🧩 PIPELINE PHẢI NHỚ

**Neural TTS:** Text → **Text Analysis** (normalization + G2P) → **Acoustic Model** (→ mel-spectrogram) → **Vocoder** (→ waveform). 3 mức E2E: modular → E2E (bỏ ranh giới) → fully E2E (text→waveform).

**ASR truyền thống:** Feature (windowing 25ms/stride 10ms → Hamming → Mel filterbank → log) → **AM + LM + Decoder**. Tiến hoá: **HMM/Viterbi → AED/LAS → CTC → RNN-T → SSL+Transformer (Whisper, Wav2Vec2)**.

**Trích đặc trưng audio:** waveform → framing/windowing → **STFT** → Mel filter bank → log → (DCT) → **MFCC**.

**Forced Alignment:** HMM-GMM (Kaldi) → DL (MFA) → CTC (Wav2Vec2) → E2E ASR (Whisper). Càng mới càng robust nhưng kém chính xác ở ranh giới phoneme mịn.

**Xây dataset:** Collection (Studio/Crowdsource/Crawl/Synthesis) → Annotation (human/weak/pseudo-label) → Forced Alignment → Processing (VAD, diarization, denoise, trim, resample 16kHz) → Augmentation (noise/RIR, speed perturbation, SpecAugment) → Benchmark (WER/CER/EER, SNR/PESQ/STOI, IAA).

---

## 📌 SỐ LIỆU & TÊN RIÊNG DỄ HỎI

- Con người WER ~**5–6%**; Google Switchboard **5.1%**.
- Whisper: **680k giờ**, **96+ ngôn ngữ**. XLSR: **53+ ngôn ngữ**. VALL-E: zero-shot prompt **3 giây**.
- Mốc bitrate: 128 kbps (MP3 chuẩn), 320 kbps (gần CD), 1411 kbps (CD).
- CD sample rate **44.1 kHz** → bắt tới **22.05 kHz**.
- Face IoU > **0.5** (face stream, Vietnam-Celeb).
- Dataset: ASR (LibriSpeech, CommonVoice, TEDLIUM, VoxPopuli) · Speaker (VoxCeleb, DIHARD) · TTS (VCTK, LibriTTS) · SER (IEMOCAP, MELD).
