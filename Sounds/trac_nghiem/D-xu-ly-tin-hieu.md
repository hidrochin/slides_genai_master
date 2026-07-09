# TRẮC NGHIỆM — Cụm D: Xử lý Tín hiệu số (16 câu)
Nguồn: `03 - Digital Signal Processing`. Ôn kèm [D-DSP](../on_tap/D-xu-ly-tin-hieu.md).

> **Cách dùng:** Phương án dài bằng nhau, không tô đậm. **(Nhiều đáp án)** = chọn đủ. **(Khó)** = nhiều bước tính/phân biệt bẫy đơn vị. Nhớ: `Size = Sample rate × Bit depth × Channels × Duration`; `mức = 2^bit`; `1 byte = 8 bit`.

---

**Câu 1.** Hai bước cốt lõi của quá trình chuyển analog → digital (ADC) là gì?
- A. Sampling (lấy mẫu) và Quantization (lượng tử hoá)
- B. Compression và Decompression
- C. Windowing và Fourier Transform
- D. Encoding và Modulation

<details><summary>Đáp án</summary>

**A.** ADC = **Sampling** (rời rạc hoá thời gian) + **Quantization** (rời rạc hoá biên độ). C là bước trích đặc trưng sau này (STFT), không phải ADC.
</details>

---

**Câu 2.** Bit depth trong audio số mô tả điều gì?
- A. Số bit dùng để biểu diễn mỗi mẫu (số mức biên độ)
- B. Số mẫu lấy được mỗi giây
- C. Số bit biểu diễn một giây audio
- D. Kích thước file tính bằng bit

<details><summary>Đáp án</summary>

**A.** **Bit depth** = số bit mỗi **mẫu** → quyết định số **mức biên độ**. B là sample rate; C là bit rate; D là file size. Đây chính là 4 phương án gây nhầm trong quiz gốc.
</details>

---

**Câu 3.** File audio bit depth 16 bit biểu diễn được bao nhiêu mức biên độ?
- A. 65 536 mức
- B. 256 mức
- C. 16 mức
- D. 1 048 576 mức

<details><summary>Đáp án</summary>

**A.** `2^16 = 65 536`. Bẫy: 256 = 2^8, 1 048 576 = 2^20, 16 = số bit chứ không phải số mức.
</details>

---

**Câu 4.** File có sample rate 96 000 mẫu/giây thì sample rate là bao nhiêu?
- A. 96 kHz
- B. 48 kHz
- C. 44.1 kHz
- D. 192 kHz

<details><summary>Đáp án</summary>

**A.** 96 000 mẫu/s = **96 kHz** (1 kHz = 1000 mẫu/s). Đơn giản nhưng dễ mất điểm nếu lẫn với Nyquist (½ hoặc ×2).
</details>

---

**Câu 5.** (Khó) File 44.1 kHz, 16 bit, stereo (2 kênh), 1 phút không nén có kích thước bao nhiêu?
- A. ≈ 10.584 MB
- B. ≈ 5.292 MB
- C. ≈ 1.41 MB
- D. ≈ 176.4 KB

<details><summary>Đáp án</summary>

**A.** `44100 × 16 × 2 × 60 = 84 672 000 bit = 10 584 000 byte ≈ 10.584 MB`. Bẫy B: quên nhân 2 kênh (chỉ mono → ~5.29 MB). Bẫy C: nhầm bit rate 1.41 Mbps thành size. Bẫy D: chỉ tính 1 giây mono.
</details>

---

**Câu 6.** (Khó) File bit rate 128 kbps, thời lượng 3 phút. Kích thước file?
- A. ≈ 2.88 MB
- B. ≈ 3.84 MB
- C. ≈ 5.76 MB
- D. ≈ 1.44 MB

<details><summary>Đáp án</summary>

**A.** `128 000 bit/s × 180 s = 23 040 000 bit ÷ 8 = 2 880 000 byte ≈ 2.88 MB`. Bẫy: quên chia 8 (ra ~23 "MB" nếu để bit), hoặc dùng 60 s thay vì 180 s.
</details>

---

**Câu 7.** (Khó) File 5 phút, 44 100 mẫu/giây, biên độ lượng tử hoá thành 1 024 mức. Kích thước (megabit)?
- A. ≈ 132.3 Mb
- B. ≈ 13.23 Mb
- C. ≈ 2.205 Mb
- D. ≈ 220 500 bit

<details><summary>Đáp án</summary>

**A.** 1024 mức = `2^10` → **10 bit/mẫu**. `44 100 × 10 × 300 s = 132 300 000 bit ≈ 132.3 Mb` (megabit, mono). Bẫy chính: dùng "1024" như số bit thay vì log₂ → sai; hoặc lẫn Mb (megabit) với MB (megabyte).
</details>

---

**Câu 8.** Định lý Nyquist–Shannon phát biểu điều gì?
- A. Sample rate phải ít nhất gấp đôi tần số cao nhất trong tín hiệu để tái tạo trung thực
- B. Sample rate phải bằng đúng tần số cao nhất trong tín hiệu
- C. Bit depth phải gấp đôi số kênh audio
- D. Bit rate phải bằng một nửa sample rate

<details><summary>Đáp án</summary>

**A.** Nyquist: `sample rate ≥ 2 × f_max`. VD tín hiệu tới 20 kHz cần sample rate ≥ 40 kHz. Không phải "bằng" (B — sẽ gây aliasing).
</details>

---

**Câu 9.** (Khó) CD dùng sample rate 44.1 kHz. Tần số cao nhất biểu diễn chính xác được (Nyquist frequency) và hệ quả nếu vi phạm là gì?
- A. 22.05 kHz; vi phạm gây aliasing → distortion
- B. 88.2 kHz; vi phạm gây tăng kích thước file
- C. 44.1 kHz; vi phạm gây mất kênh stereo
- D. 20 kHz; vi phạm gây giảm bit depth

<details><summary>Đáp án</summary>

**A.** Nyquist frequency = **½ sample rate = 22.05 kHz** → phủ dải nghe người (20 Hz–20 kHz). Nếu sample rate quá thấp so với tín hiệu → **aliasing → distortion (méo)**. B nhầm ×2 thay vì ÷2.
</details>

---

**Câu 10.** (Nhiều đáp án) Đâu là các định dạng nén LOSSY (mất dữ liệu)?
- A. MP3
- B. AAC
- C. Opus
- D. FLAC
- E. WAV

<details><summary>Đáp án</summary>

**A, B, C.** MP3, AAC, OGG, **Opus** là **lossy** (loại bỏ vĩnh viễn thông tin, nhỏ 70-90%). FLAC/ALAC là **lossless**; WAV/AIFF là **uncompressed**.
</details>

---

**Câu 11.** So với nén lossless, nén lossy khác biệt cơ bản ở điểm nào?
- A. Lossy loại bỏ vĩnh viễn thông tin ít quan trọng; lossless giữ nguyên chất lượng gốc
- B. Lossy giữ nguyên chất lượng gốc; lossless loại bỏ thông tin
- C. Cả hai đều không thay đổi chất lượng, chỉ khác tốc độ mã hoá
- D. Lossy chỉ áp dụng cho video, lossless chỉ cho audio

<details><summary>Đáp án</summary>

**A.** Lossy = **bỏ vĩnh viễn** phần âm ít quan trọng/ít nghe thấy (đổi lấy file nhỏ); lossless = **giữ nguyên** chất lượng gốc (nhỏ 30-70%). B đảo ngược.
</details>

---

**Câu 12.** Ba thông tin cơ bản của waveform — Frequency, Intensity, Timbre — lần lượt liên quan tri giác nào?
- A. Cao/thấp (pitch); to/nhỏ (loudness); màu âm phân biệt hai âm cùng tần số & cường độ
- B. To/nhỏ; cao/thấp; độ dài âm
- C. Màu âm; cao/thấp; to/nhỏ
- D. Độ dài; màu âm; cao/thấp

<details><summary>Đáp án</summary>

**A.** **Frequency** → cao/thấp (pitch); **Intensity** → to/nhỏ (loudness); **Timbre** → "màu"/chất âm phân biệt hai âm dù cùng frequency & intensity.
</details>

---

**Câu 13.** Ba miền biểu diễn tín hiệu audio là gì?
- A. Time domain, Frequency domain, Time-Frequency domain
- B. Analog, Digital, Hybrid
- C. Mono, Stereo, Surround
- D. Lossy, Lossless, Uncompressed

<details><summary>Đáp án</summary>

**A.** **Time** (waveform theo thời gian), **Frequency** (thành phần tần số qua Fourier), **Time-Frequency** (đồng thời — nội dung tần số tiến hoá theo thời gian, VD spectrogram).
</details>

---

**Câu 14.** (Khó) Nhược điểm chính của STFT so với các phương pháp time-frequency khác là gì?
- A. Fixed resolution — dùng cùng kích thước cửa sổ cho mọi tần số, giới hạn trade-off time↔frequency
- B. Không tạo được spectrogram
- C. Chỉ dùng được cho tín hiệu radar
- D. Không thể chia tín hiệu thành các cửa sổ chồng lấn

<details><summary>Đáp án</summary>

**A.** STFT chia tín hiệu thành **cửa sổ chồng lấn** rồi Fourier từng cửa sổ → tạo spectrogram, nhưng **fixed resolution** (cùng window size mọi tần) ⇒ đánh đổi phân giải time-frequency bị giới hạn. Wavelet mới có adaptive resolution. B, D mô tả sai chính cơ chế STFT.
</details>

---

**Câu 15.** (Khó) Mel spectrogram khác spectrogram thường và có nhược điểm gì?
- A. Trục tần số ánh xạ sang thang Mel (khớp tri giác người), nhưng không giữ thông tin tần số thô (raw frequency)
- B. Trục thời gian bị nén, giữ nguyên toàn bộ raw frequency
- C. Chỉ khác về màu sắc hiển thị, bản chất giống hệt spectrogram
- D. Không dùng được cho machine learning

<details><summary>Đáp án</summary>

**A.** Mel spectrogram ánh xạ trục y sang **thang Mel** (xấp xỉ tri giác pitch của người) → gọn, hợp ML; nhược: **không giữ raw frequency**. D sai hẳn (Mel spec chính là feature ưa dùng cho DL audio).
</details>

---

**Câu 16.** MFCC (Mel-Frequency Cepstral Coefficients) được thiết kế để làm gì?
- A. Nén power spectrum thành đặc trưng gọn, xấp xỉ cách con người tri giác âm (thang Mel)
- B. Tăng kích thước dữ liệu audio để train tốt hơn
- C. Thay thế hoàn toàn sample rate và bit depth
- D. Chuyển waveform thành văn bản trực tiếp

<details><summary>Đáp án</summary>

**A.** MFCC = biểu diễn **gọn** của power spectrum, gắn thang **Mel** (tri giác người), giảm dữ liệu nhiều chiều thành ít hệ số có nghĩa (qua khái niệm **cepstrum**). Không phải để tăng dữ liệu (B) hay chuyển thành text (D — đó là ASR).
</details>
