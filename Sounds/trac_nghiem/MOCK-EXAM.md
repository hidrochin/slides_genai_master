# MOCK EXAM — Đề tổng hợp Tạo sinh Âm thanh (30 câu, trộn cụm)

> **Cách dùng:** Đề mô phỏng thi thật — trộn ngẫu nhiên các cụm A→H, độ khó tăng dần, nhiều câu tính toán & **(Nhiều đáp án)**. Làm liền mạch, tự chấm cuối. Mục tiêu ≥ 24/30. Chi tiết lý thuyết ở thư mục [../on_tap/](../on_tap/00-ONE-PAGER.md).

---

**Câu 1.** Ba nhánh của Phonetics là gì?
- A. Articulatory, Acoustic, Auditory
- B. Phonology, Morphology, Syntax
- C. Time, Frequency, Time-Frequency
- D. Place, Manner, Voicing

<details><summary>Đáp án</summary>

**A.** Production / physical / perception. D là ba chiều phân loại phụ âm; C là ba miền tín hiệu.
</details>

---

**Câu 2.** (Nhiều đáp án) Cặp phụ âm nào chỉ khác nhau ở voicing (cùng place & manner)?
- A. /b/ – /p/
- B. /z/ – /s/
- C. /v/ – /f/
- D. /m/ – /s/
- E. /d/ – /t/

<details><summary>Đáp án</summary>

**A, B, C, E.** Bốn cặp voiced–unvoiced. D sai: /m/ (nasal stop, voiced) và /s/ (fricative, unvoiced) khác cả manner lẫn voicing.
</details>

---

**Câu 3.** (Khó) File audio 48 kHz, 24 bit, mono, 10 giây. Kích thước không nén?
- A. ≈ 1.44 MB
- B. ≈ 2.88 MB
- C. ≈ 11.52 MB
- D. ≈ 720 KB

<details><summary>Đáp án</summary>

**A.** `48000 × 24 × 1 × 10 = 11 520 000 bit ÷ 8 = 1 440 000 byte ≈ 1.44 MB`. Bẫy C: quên chia 8. Bẫy B: nhân nhầm 2 kênh.
</details>

---

**Câu 4.** Nyquist frequency của hệ lấy mẫu ở 16 kHz (chuẩn cho ASR) là bao nhiêu?
- A. 8 kHz
- B. 16 kHz
- C. 32 kHz
- D. 4 kHz

<details><summary>Đáp án</summary>

**A.** Nyquist frequency = ½ sample rate = **8 kHz**. Nghĩa là tín hiệu tới 8 kHz được biểu diễn chính xác.
</details>

---

**Câu 5.** Công thức WER là gì?
- A. (S + D + I) / N
- B. (S + D + I) × N
- C. (S − D + I) / N
- D. (S + D) / (I + N)

<details><summary>Đáp án</summary>

**A.** Substitutions + Deletions + Insertions, chia số từ reference N.
</details>

---

**Câu 6.** (Khó) Reference 8 từ, ASR mắc 1 substitution, 2 deletions, 1 insertion. WER?
- A. 0.5
- B. 0.375
- C. 0.25
- D. 0.4

<details><summary>Đáp án</summary>

**A.** `(1 + 2 + 1) / 8 = 4/8 = 0.5`. Bẫy B: quên insertion (3/8). Bẫy: đừng chia cho số từ ASR output.
</details>

---

**Câu 7.** Cấu trúc âm tiết tiếng Việt là gì?
- A. (C1)(w)V(C2)-T
- B. C-V-C
- C. (C1)(C2)V
- D. V-T-C

<details><summary>Đáp án</summary>

**A.** Âm đầu, âm đệm /w/, âm chính (bắt buộc), âm cuối, thanh (T). Tiếng Việt không có cụm 2 phụ âm đầu.
</details>

---

**Câu 8.** (Nhiều đáp án) Đâu là định dạng nén lossless?
- A. FLAC
- B. ALAC
- C. MP3
- D. WAV
- E. Opus

<details><summary>Đáp án</summary>

**A, B.** FLAC, ALAC = lossless. MP3/Opus = lossy; WAV = uncompressed.
</details>

---

**Câu 9.** RTF = 0.25 nghĩa là gì?
- A. Hệ tổng hợp nhanh gấp 4 lần real-time
- B. Hệ chậm gấp 4 lần real-time
- C. Hệ tổng hợp đúng bằng real-time
- D. Hệ có độ trễ 25 giây

<details><summary>Đáp án</summary>

**A.** RTF = t_synth/t_audio = 0.25 < 1 → nhanh hơn real-time; 1/0.25 = **4× real-time**.
</details>

---

**Câu 10.** (Khó) Điền vào công thức ASR: Ŵ = argmax P(X|W)·P(W). P(X|W) và P(W) lần lượt là gì?
- A. Acoustic Model và Language Model
- B. Language Model và Acoustic Model
- C. Vocoder và Decoder
- D. Prior và Posterior

<details><summary>Đáp án</summary>

**A.** P(X|W) = **Acoustic Model** (likelihood của quan sát X cho chuỗi từ W); P(W) = **Language Model** (prior của chuỗi từ).
</details>

---

**Câu 11.** Thứ tự đúng pipeline TTS hiện đại?
- A. Text Analysis → Acoustic Model → Vocoder
- B. Vocoder → Acoustic Model → Text Analysis
- C. Acoustic Model → Vocoder → Text Analysis
- D. Text Analysis → Vocoder → Acoustic Model

<details><summary>Đáp án</summary>

**A.** Frontend (normalization + G2P) → Acoustic Model (→ mel) → Vocoder (→ waveform).
</details>

---

**Câu 12.** (Nhiều đáp án) Metric nào là subjective (dựa tri giác người) trong đánh giá TTS?
- A. MOS
- B. CMOS
- C. SMOS
- D. MCD
- E. RTF

<details><summary>Đáp án</summary>

**A, B, C.** MOS/CMOS/SMOS = subjective. MCD & RTF = objective (tính được).
</details>

---

**Câu 13.** (Khó) EER trong Speaker Verification là điểm mà:
- A. FAR = FRR, và EER thấp là hệ tốt
- B. FAR = 0
- C. Accuracy = 100%
- D. FRR = 2 × FAR

<details><summary>Đáp án</summary>

**A.** Equal Error Rate = giao điểm FAR (false accept) và FRR (false reject); **thấp = tốt hơn**.
</details>

---

**Câu 14.** Bit depth 24 bit biểu diễn được bao nhiêu mức biên độ?
- A. 16 777 216 mức
- B. 65 536 mức
- C. 256 mức
- D. 24 mức

<details><summary>Đáp án</summary>

**A.** `2^24 = 16 777 216`. (2^16 = 65 536 là 16 bit.)
</details>

---

**Câu 15.** (Nhiều đáp án) Ưu điểm của End-to-End TTS?
- A. Tối thiểu annotation tay
- B. Không cần alignment tường minh text-speech
- C. Không error propagation (một model duy nhất)
- D. Không cần dữ liệu train
- E. Loại bỏ hoàn toàn thanh điệu

<details><summary>Đáp án</summary>

**A, B, C.** D sai (vẫn cần cặp text-speech); E sai (thanh điệu bắt buộc cho tiếng Việt).
</details>

---

**Câu 16.** (Khó) CTC Problem 2 ("outputs độc lập") gây hậu quả gì?
- A. Sinh output vô lý ngữ pháp kiểu "I eight food", cần search + LM phụ để sửa
- B. Output luôn dài hơn input
- C. Không thể dùng blank token
- D. Bắt buộc forced alignment frame-level

<details><summary>Đáp án</summary>

**A.** Giả định độc lập giữa các output → "I eight food" thay vì "I ate food"; cần secondary LM. RNN-T thêm Predictor để giải.
</details>

---

**Câu 17.** Vì sao RNN-T hợp streaming hơn CTC?
- A. RNN-T emit token-by-token khi audio đang tới, còn CTC thường chờ cả chunk rồi collapse
- B. CTC nhanh hơn và context-aware hơn RNN-T
- C. RNN-T cần cả câu trước khi decode
- D. Cả hai đều không hỗ trợ streaming

<details><summary>Đáp án</summary>

**A.** RNN-T incremental output + Predictor (context-aware). CTC hay chờ collapse repeated tokens → trễ hơn.
</details>

---

**Câu 18.** Whisper được train trên bao nhiêu giờ và bao nhiêu ngôn ngữ?
- A. 680k giờ, 96+ ngôn ngữ
- B. 53 giờ, 1 ngôn ngữ
- C. 1000 giờ, 10 ngôn ngữ
- D. 680 giờ, 2 ngôn ngữ

<details><summary>Đáp án</summary>

**A.** 680k giờ, 96+ ngôn ngữ, multilingual ASR + translation out-of-the-box.
</details>

---

**Câu 19.** (Nhiều đáp án) Phương pháp thu thập dữ liệu tiếng nói?
- A. Studio recording
- B. Crowdsourced
- C. Crawling
- D. Synthesis
- E. Forced alignment

<details><summary>Đáp án</summary>

**A, B, C, D.** E (forced alignment) là bước **gán nhãn/căn chỉnh**, không phải thu thập.
</details>

---

**Câu 20.** (Khó) SNR, PESQ, STOI thuộc nhóm tiêu chí nào của dataset?
- A. Data Quality & Cleanliness
- B. Diversity
- C. Balance & Bias
- D. Labeling Accuracy

<details><summary>Đáp án</summary>

**A.** Ba metric đo chất lượng/độ sạch (SNR cao = tốt, PESQ = tri giác, STOI = intelligibility trong nhiễu).
</details>

---

**Câu 21.** VALL-E cần prompt bao lâu để zero-shot voice cloning?
- A. ~3 giây
- B. ~30 phút
- C. ~1 giờ
- D. ~10 giây

<details><summary>Đáp án</summary>

**A.** ~3 giây; dự đoán mã RVQ rời rạc thay vì spectrogram.
</details>

---

**Câu 22.** (Nhiều đáp án) Đặc điểm của Mel spectrogram?
- A. Trục tần số ánh xạ sang thang Mel (khớp tri giác người)
- B. Gọn, hiệu quả cho machine learning
- C. Không giữ thông tin raw frequency
- D. Giữ toàn bộ raw frequency với độ phân giải tuyến tính
- E. Chỉ dùng cho video, không dùng cho audio

<details><summary>Đáp án</summary>

**A, B, C.** D mâu thuẫn C; E sai (Mel spec là feature audio phổ biến cho DL).
</details>

---

**Câu 23.** (Khó) Nối 4 loại MOS: "Which one is better?" ứng với loại nào?
- A. CMOS
- B. MOS
- C. DMOS
- D. SMOS

<details><summary>Đáp án</summary>

**A.** CMOS (Comparative, −3..+3). MOS = "tốt cỡ nào"; DMOS = "xuống cấp cỡ nào"; SMOS = "giống style/speaker không".
</details>

---

**Câu 24.** Âm đệm duy nhất /w/ của tiếng Việt viết bằng "o" khi nào?
- A. Khi đứng trước nguyên âm rộng (a, ă, e)
- B. Khi đứng trước i, ê, ơ, â
- C. Luôn luôn viết "o"
- D. Chỉ trong từ vay mượn

<details><summary>Đáp án</summary>

**A.** "o" trước nguyên âm rộng (toát, hoè); "u" trước y, ê, ơ, â (huy, Huế).
</details>

---

**Câu 25.** (Khó) File 44.1 kHz, 16 bit, stereo, dài 2 phút. Kích thước?
- A. ≈ 21.17 MB
- B. ≈ 10.584 MB
- C. ≈ 42.34 MB
- D. ≈ 5.29 MB

<details><summary>Đáp án</summary>

**A.** 1 phút ≈ 10.584 MB (đã tính ở cụm D) → 2 phút ≈ **21.17 MB**. Bẫy B: chỉ 1 phút; Bẫy D: mono 1 phút.
</details>

---

**Câu 26.** (Nhiều đáp án) Kỹ thuật augmentation dữ liệu tiếng nói?
- A. Speed perturbation (giữ nguyên pitch)
- B. SpecAugment (masking spectrogram)
- C. Room simulation (RIR)
- D. Pseudo labeling
- E. Silence trimming

<details><summary>Đáp án</summary>

**A, B, C.** D là gán nhãn; E là tiền xử lý (không phải augment tạo biến thể).
</details>

---

**Câu 27.** Grapheme khác Phoneme thế nào?
- A. Grapheme = đơn vị viết nhỏ nhất; Phoneme = đơn vị âm nhỏ nhất
- B. Grapheme = đơn vị âm; Phoneme = đơn vị viết
- C. Cả hai đều là đơn vị âm thanh
- D. Cả hai đều là đơn vị viết

<details><summary>Đáp án</summary>

**A.** Grapheme viết (th, ngh); Phoneme âm (/θ/, /ŋ/). Allophone [ ] là biến thể của phoneme.
</details>

---

**Câu 28.** (Khó) F0 của waveform có 20 chu kỳ trong 0.1 giây là bao nhiêu?
- A. 200 Hz
- B. 20 Hz
- C. 2000 Hz
- D. 100 Hz

<details><summary>Đáp án</summary>

**A.** `F0 = 20 / 0.1 = 200 Hz`. F0 = số chu kỳ / thời gian.
</details>

---

**Câu 29.** (Nhiều đáp án) Bốn thành phần kiến trúc ASR truyền thống?
- A. Acoustic Model
- B. Language Model
- C. Decoder
- D. Adaptation
- E. Griffin-Lim vocoder

<details><summary>Đáp án</summary>

**A, B, C, D.** Griffin-Lim là **vocoder** thuộc TTS, không có trong kiến trúc ASR.
</details>

---

**Câu 30.** (Khó) Sắp xếp tiến hoá kỹ thuật ASR theo thời gian tăng dần?
- A. Template Matching → HMM → GMM-HMM → CTC/RNN-T → SSL+Transformer
- B. SSL+Transformer → CTC → HMM → Template Matching
- C. HMM → Template Matching → SSL → GMM-HMM
- D. GMM-HMM → Template Matching → RNN-T → HMM

<details><summary>Đáp án</summary>

**A.** 1950s → 1980s → 1990s → 2010s → 2020s. Whisper/Wav2Vec2 là giai đoạn SSL+Transformer mới nhất.
</details>

---

### Bảng tự chấm nhanh
| Cụm | Câu |
|---|---|
| B (Ngữ âm) | 1, 2, 27, 28 |
| D (DSP) | 3, 4, 8, 14, 25 |
| F (Đánh giá) | 5, 6, 9, 12, 13, 23 |
| C (Tiếng Việt) | 7, 24 |
| H (ASR) | 10, 16, 17, 18, 29, 30 |
| G (TTS) | 11, 15, 21, 22 |
| E (Dữ liệu) | 19, 20, 26 |

Sai câu nào → mở file on_tap tương ứng theo bảng. Ưu tiên ôn lại cụm sai ≥ 2 câu.
