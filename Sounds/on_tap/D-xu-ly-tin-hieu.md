# D — Xử lý Tín hiệu số cho Tiếng nói (Digital Signal Processing)

> Nguồn: `03 - Digital Signal Processing`. Cụm NHIỀU TÍNH TOÁN: sample rate, bit depth, bit rate, kích thước file, Nyquist, nén, biểu diễn tín hiệu, STFT/Mel/MFCC.

Điều hướng: [00-ONE-PAGER](00-ONE-PAGER.md) · [B-ngữ-âm-học](B-ngu-am-hoc.md) · [E-dữ-liệu](E-du-lieu.md) · [H-nhận-dạng](H-nhan-dang-tieng-noi.md)

---

## 1. Số hoá âm thanh: ADC (Analogue-to-Digital Converter)

Tín hiệu **analog** = giá trị **liên tục**. Chuyển sang digital gồm **2 bước**:
1. **Sampling (lấy mẫu):** chuyển tín hiệu thời gian liên tục → biểu diễn **thời gian rời rạc**, tại các **sampling interval**.
2. **Quantization (lượng tử hoá):** ánh xạ giá trị **biên độ liên tục** → **tập giá trị rời rạc** (sau sampling).

## 2. Ba đại lượng cốt lõi — PHẢI PHÂN BIỆT RÕ

| Đại lượng | Định nghĩa | Đơn vị |
|---|---|---|
| **Sample rate (tần số lấy mẫu)** | Số lần lấy mẫu **mỗi giây** | Hz / kHz |
| **Bit depth (độ sâu bit)** | Số **bit biểu diễn mỗi mẫu** (số mức biên độ) | bit |
| **Bit rate (tốc độ bit)** | Số **bit biểu diễn mỗi giây** audio | bit/s (bps) |

- **Sampling interval nhỏ ⇔ sample rate cao ⇔ chất lượng cao ⇔ file lớn hơn.**
- **Bit depth:** n bit → **2ⁿ mức biên độ**. VD 16 bit → **65 536 mức** (= 2¹⁶). (8 bit → 256; 24 bit → ~16.7 triệu.)

## 3. CÔNG THỨC PHẢI NHỚ (dạng bài tính)

```
Bit rate = Bit depth × Sample rate × Số kênh (channels)
File size (bit) = Bit rate × Thời lượng (s)
              = Sample rate × Bit depth × Channels × Duration
```

Đổi đơn vị: **1 byte = 8 bit**; 1 KB = 1024 byte (hoặc 1000 tuỳ quy ước bài); 1 MB = 1024 KB.

### Ví dụ mẫu (giải kỹ):
- **CD 44.1 kHz, 16 bit, stereo (2 kênh), 1 phút (60 s):**
  Bit rate = 44100 × 16 × 2 = 1 411 200 bps ≈ **1 411 kbps** (đúng "CD quality").
  Size = 1 411 200 × 60 = 84 672 000 bit = 10 584 000 byte ≈ **10.584 MB**.
- **File 128 kbps, 3 phút:** 128 000 × 180 = 23 040 000 bit ÷ 8 = 2 880 000 byte ≈ **2.88 MB**.
- **96 kHz, 24 bit, stereo, file 50 MB → thời lượng?** Bit rate = 96000×24×2 = 4 608 000 bps. Size bit = 50×8×10⁶ = 400 000 000. Duration = 400 000 000 / 4 608 000 ≈ **86.8 s ≈ 1 phút 27 s** (chú ý cách quy MB của đề!).
- **5 phút, 44100 mẫu/s, lượng tử 1024 mức → size?** 1024 mức = 2¹⁰ ⇒ **10 bit/mẫu**. Bit rate = 44100×10 = 441 000 bps. Size = 441 000 × 300 = **132 300 000 bit ≈ 132.3 Mb** (mega**bit**).

> **Bẫy đơn vị:** "Mb" (megabit) ≠ "MB" (megabyte). Số **mức** → quy ra **bit** bằng log₂(mức). Nhớ nhân **số kênh**.

## 4. Nyquist–Shannon Sampling Theorem — HAY HỎI LÝ THUYẾT

- **Định lý:** để **tái tạo trung thực** một tín hiệu từ mẫu của nó, **sample rate ≥ 2× tần số cao nhất** trong tín hiệu.
  - VD: tín hiệu tới 20 kHz → cần sample rate **≥ 40 kHz**.
- **Nyquist rate/frequency:** tần số **tối đa** biểu diễn chính xác được = **½ sample rate**.
  - CD 44.1 kHz → bắt được tới **22.05 kHz**, phủ dải nghe người (20 Hz–20 kHz).
- **Nếu vi phạm (sample rate quá thấp)** → **Aliasing → Distortion (méo).**

## 5. Nén (Compression) — bảng so sánh

| | **Lossy** | **Lossless** | **Uncompressed** |
|---|---|---|---|
| Kích thước | Nhỏ **70–90%** | Nhỏ **30–70%** | Rất lớn |
| Chất lượng | **Giảm** (tuỳ bitrate) | **Nguyên gốc** | Nguyên gốc |
| Use case | Streaming, lưu di động | Archiving, chuyên nghiệp | Audiophile, chuyên nghiệp |
| Ví dụ | **MP3, AAC, OGG, Opus** | **FLAC, ALAC** | **WAV, AIFF** |

- **Lossy** = loại bỏ **vĩnh viễn** thông tin âm ít quan trọng/ít nghe thấy → cân bằng size & chất lượng.
- **Mốc bitrate cần nhớ:** 96 kbps (thấp) · 128 kbps (chuẩn MP3) · 256 kbps (cao, Apple Music) · 320 kbps (gần CD) · **1 411 kbps = CD** (44.1 kHz/16 bit/stereo) · 4 608 kbps (hi-res 96 kHz/24 bit).

## 6. Biểu diễn tín hiệu (Signal Representation)

### 6.1 Ba thông tin cơ bản của waveform
- **Frequency (tần số):** âm "cao" hay "thấp" (pitch).
- **Intensity (cường độ):** âm "to" hay "nhỏ".
- **Timbre (âm sắc):** "màu sắc" riêng phân biệt hai âm cùng tần số & cường độ.

### 6.2 Ba miền biểu diễn — PHÂN BIỆT
- **Time Domain:** tín hiệu biến thiên **theo thời gian** (waveform).
- **Frequency Domain:** mô tả theo **thành phần tần số**, dùng **Fourier Transform**.
- **Time-Frequency Domain:** đồng thời **cả thời gian và tần số** — cho biết **nội dung tần số tiến hoá ra sao theo thời gian**.

### 6.3 Các phương pháp Time-Frequency — bảng so sánh
| Method | Resolution | Ứng dụng | Điểm mạnh | Điểm yếu |
|---|---|---|---|---|
| **STFT** | Cố định time-freq | Speech, music | Đơn giản, phổ biến | Trade-off phân giải bị giới hạn |
| **Wavelet** | Thích nghi (adaptive) | Biomedical, tín hiệu transient | Tốt cho transient | Phức tạp tính toán |
| **Wigner-Ville** | Cao | Radar, cơ học lượng tử | Phân giải cao | Nhiễu cross-term |
| **Mel Spectrogram** | Theo thang Mel | Speech recognition, AI | Khớp tri giác người | Ít thông tin tần số thô |
| **Constant-Q** | Logarithmic | Music transcription | Hợp phân tích cao độ | Nặng tính toán |

## 7. STFT → Spectrogram

- **STFT (Short-Time Fourier Transform):** chia tín hiệu thành **cửa sổ thời gian nhỏ, chồng lấn (overlapping windows/segments)** rồi áp Fourier cho từng cửa sổ → tạo **spectrogram** (phổ tần biến thiên theo thời gian).
- **Ưu:** dễ cài, phổ biến. **Nhược:** **fixed resolution** — cùng một kích thước cửa sổ cho mọi tần số ⇒ giới hạn trade-off time↔frequency.

## 8. Mel Spectrogram & MFCC — RẤT HAY HỎI (đặc trưng cho ML)

- **Mel scale:** thang tần số **xấp xỉ cách người tri giác cao độ (pitch)**.
- **Mel Spectrogram:** biến thể spectrogram, **trục y ánh xạ sang thang Mel**.
  - **Ưu:** khớp tri giác thính giác người; **gọn & hiệu quả** cho ML.
  - **Nhược:** **KHÔNG giữ thông tin tần số thô (raw frequency).**
- **MFCC (Mel-Frequency Cepstral Coefficients):** biểu diễn **gọn** của **power spectrum**, thiết kế để **xấp xỉ tri giác người (Mel scale)** → nén dữ liệu audio nhiều chiều thành đặc trưng gọn, có nghĩa. (Khái niệm nền: **cepstrum**.)

> **Chuỗi trích đặc trưng điển hình:** waveform → framing (windowing) → STFT → Mel filter bank → log → (DCT) → **MFCC**. (Chi tiết windowing/Hamming/Mel filterbank ở [H-nhận-dạng](H-nhan-dang-tieng-noi.md).)

---

## 🎓 Mở rộng nâng cao (trình độ thạc sĩ — ngoài slide)

### N1. Fourier: DTFT → DFT → FFT
- **DTFT** của tín hiệu rời rạc `x[n]`: `X(e^{jω}) = Σₙ x[n] e^{-jωn}` — phổ **liên tục & tuần hoàn 2π**.
- **DFT** (lấy N mẫu phổ): `X[k] = Σ_{n=0}^{N-1} x[n] e^{-j2πkn/N}`, k = 0..N−1. Độ phân giải tần số `Δf = f_s / N` → muốn mịn hơn thì **N lớn** (cửa sổ dài) ⇒ đánh đổi thời gian (xem N3).
- **FFT** = thuật toán tính DFT trong `O(N log N)` thay vì `O(N²)` (Cooley–Tukey), nền tảng khiến STFT khả thi real-time.
- **Power spectrum** = `|X[k]|²`; ước lượng thực tế dùng **periodogram/Welch** (trung bình nhiều đoạn để giảm phương sai).

### N2. Định lý lấy mẫu — vì sao và aliasing (dạng gập)
- Lấy mẫu ở `f_s` làm **phổ lặp lại (replication)** mỗi `f_s`. Nếu băng thông tín hiệu `> f_s/2`, các bản sao **chồng lấn** → **aliasing** không thể gỡ.
- **Công thức gập:** tần số `f` hiện ra ở `f_alias = |f − k·f_s|` sao cho rơi vào `[0, f_s/2]` (k nguyên gần nhất). VD 30 kHz @ 44.1 kHz → 14.1 kHz.
- Thực tế: **anti-aliasing low-pass filter** trước ADC + **reconstruction filter** sau DAC (nội suy sinc lý tưởng).

### N3. Nhiễu lượng tử hoá & SNR — chứng minh "6.02·N"
- Lượng tử đều bước `Δ`: sai số coi như phân bố đều `[−Δ/2, Δ/2]` → **phương sai nhiễu** `σ² = Δ²/12`.
- Với tín hiệu full-scale biên độ `A = 2^{N-1}·Δ`, tỉ số công suất cho: **`SNR = 6.02·N + 1.76 dB`** (giả định sine full-scale). Đây là dạng chính xác của quy tắc thô `≈6.02·N` ở [§ trên]. Mỗi bit thêm ≈ **6 dB** dynamic range.

### N4. Cửa sổ & nguyên lý bất định (Gabor limit)
- Không thể phân giải đồng thời chính xác cả thời gian lẫn tần số: **`Δt · Δf ≥ 1/(4π)`** — STFT có **phân giải cố định** (cửa sổ dài ⇒ Δf nhỏ, Δt lớn); **wavelet** cho phân giải thích nghi.
- Chọn cửa sổ = đánh đổi **main-lobe width (phân giải)** ↔ **side-lobe level (spectral leakage)**: Rectangular main-lobe hẹp nhưng side-lobe cao (−13 dB); **Hann/Hamming** side-lobe thấp (−31/−43 dB) nhưng main-lobe rộng gấp đôi.
- **Pre-emphasis** `y[n] = x[n] − α·x[n−1]` (α≈0.97) trước framing để nâng năng lượng tần cao (bù dốc −6 dB/octave của nguồn thanh môn).

### N5. Mel scale & MFCC — công thức đầy đủ
- **Thang Mel:** `mel(f) = 2595·log₁₀(1 + f/700)` (xấp xỉ tri giác cao độ, gần tuyến tính <1 kHz, log ở tần cao).
- **Mel filterbank:** ~26–40 bộ lọc **tam giác** chồng lấn, đều nhau **trên trục Mel** (⇒ mịn ở tần thấp, thô ở tần cao); mỗi lọc gộp năng lượng thành 1 hệ số → lấy **log** (nén dynamic range, gần Weber–Fechner).
- **MFCC:** `MFCC = DCT(log mel-energies)`, giữ ~13 hệ số đầu. **DCT** để **khử tương quan** giữa các dải Mel (⇒ ma trận hiệp phương sai gần chéo → hợp GMM chéo) và **tách envelope (biến thiên chậm) khỏi fine structure**. Thêm **Δ, ΔΔ** (đạo hàm bậc 1,2) để mã hoá động học thời gian. **Cepstral liftering / CMVN** (mean-variance normalization) để bền với kênh thu.
- **Vì sao DL hiện đại chuộng log-mel hơn MFCC:** CNN/Transformer tự học tương quan → không cần DCT khử tương quan; MFCC làm mất thông tin. MFCC vẫn ngự trị thời **GMM-HMM** (cần feature khử tương quan).

### N6. Filterbank vs codec — hai "nén" khác nhau
- **Nén perceptual (MP3/AAC/Opus):** bỏ thông tin **dưới ngưỡng nghe** (psychoacoustic masking: masking tần số & thời gian) → không phục vụ ML mà phục vụ tai người.
- **Feature (MFCC/mel):** "nén" nhằm **giữ thông tin phân biệt âm vị**, bỏ pha & chi tiết dư — mục tiêu khác hẳn codec.
