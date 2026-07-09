# TRẮC NGHIỆM — Cụm I: Bài tập & Công thức Tính toán (22 câu, Khó → Cực khó)

Nguồn: tổng hợp công thức xuyên các cụm (DSP, Ngữ âm, Đánh giá) + dạng bài hay hỏi trong đề. Ôn kèm [ONE-PAGER](../on_tap/00-ONE-PAGER.md).

> **Cách dùng:** Đây là tệp **luyện tính** — mọi câu đều nhiều bước hoặc gài **bẫy đơn vị** (bit↔byte, Mb↔MB, log cơ số 10 vs hệ số 10/20, chu kỳ↔tần số). Tự bấm máy **trước** khi mở đáp án. Phương án sai đều là kết quả của một lỗi tính cụ thể (quên ÷8, đảo tử/mẫu, dùng nhầm hệ số dB…).

**Bộ công thức lõi:**
`Size(bit) = Sample_rate × Bit_depth × Channels × Duration` · `1 byte = 8 bit` · `mức = 2^bit`, `bit = log₂(mức)`
`Bit_rate = Sample_rate × Bit_depth × Channels` · `Size = Bit_rate × Duration`
`Nyquist_freq = Sample_rate / 2` · alias: gập f về khoảng `[0, fs/2]` · `SNR(dB) ≈ 6.02 × bit`
`F0 = số_chu_kỳ / thời_gian = 1/T` · `harmonic_n = n × F0`
`ΔL_intensity(dB) = 10·log₁₀(I₁/I₂)` · `ΔL_amplitude(dB) = 20·log₁₀(A₁/A₂)`
`WER = (S+D+I)/N_ref` · `WAcc = 1 − WER` · `RTF = t_xử_lý / t_audio` · `Perplexity = 2^(cross-entropy bit)`
`Số_frame = ⌊(N_mẫu − frame_len)/hop⌋ + 1`

---

## §1 — Âm thanh số & DSP

**Câu 1.** (Khó) File 22.05 kHz, 8-bit, mono, 30 giây (không nén). Kích thước xấp xỉ?
- A. ≈ 661.5 KB
- B. ≈ 5.29 MB
- C. ≈ 1.32 MB
- D. ≈ 82.7 KB

<details><summary>Đáp án</summary>

**A.** `22050 × 8 × 1 × 30 = 5 292 000 bit ÷ 8 = 661 500 byte ≈ 661.5 KB`. Bẫy B: **quên ÷8** (để nguyên ~5.29 "MB" ở đơn vị bit). Bẫy C: nhân nhầm 2 kênh. Bẫy D: chia 8 hai lần.
</details>

---

**Câu 2.** (Khó) Tính bit rate của chuẩn CD: 44.1 kHz, 16-bit, stereo.
- A. 1411.2 kbps
- B. 705.6 kbps
- C. 176.4 kbps
- D. 2822.4 kbps

<details><summary>Đáp án</summary>

**A.** `Bit_rate = 44100 × 16 × 2 = 1 411 200 bps = 1411.2 kbps`. Bẫy B: quên ×2 kênh (mono → 705.6). Đây là con số "1411 kbps" quen thuộc của CD.
</details>

---

**Câu 3.** (Cực khó) File MP3 128 kbps, dài 4 phút. Kích thước, và tỉ lệ nén so với CD (1411.2 kbps) là bao nhiêu?
- A. ≈ 3.84 MB; nén ≈ 11 lần
- B. ≈ 30.7 MB; nén ≈ 11 lần
- C. ≈ 3.84 MB; nén ≈ 5 lần
- D. ≈ 0.96 MB; nén ≈ 11 lần

<details><summary>Đáp án</summary>

**A.** `128 000 × 240 s = 30 720 000 bit ÷ 8 = 3 840 000 byte ≈ 3.84 MB`. Tỉ lệ nén = `1411.2 / 128 ≈ 11×`. Bẫy B: quên ÷8; bẫy D: dùng 60 s thay 240 s.
</details>

---

**Câu 4.** (Khó) Để lượng tử hoá biên độ thành 4096 mức, cần bit depth bao nhiêu?
- A. 12 bit
- B. 4096 bit
- C. 10 bit
- D. 16 bit

<details><summary>Đáp án</summary>

**A.** `bit = log₂(4096) = 12` (vì 2¹² = 4096). Bẫy C: 10 bit = 1024 mức; bẫy D: 16 bit = 65 536 mức. Số mức là **luỹ thừa** của bit, không phải bằng bit (B).
</details>

---

**Câu 5.** (Cực khó) Tín hiệu thuần 25 kHz được lấy mẫu ở 30 kHz (không có anti-aliasing filter). Nó xuất hiện ở tần số nào sau ADC?
- A. 5 kHz
- B. 25 kHz
- C. 15 kHz
- D. 55 kHz

<details><summary>Đáp án</summary>

**A.** Nyquist freq = 30/2 = 15 kHz. 25 kHz **vượt** ngưỡng → gập: `f_alias = f_s − f = 30 − 25 = 5 kHz`. Bẫy B: tưởng giữ nguyên; bẫy C: tưởng bị "chặn" đúng ở Nyquist.
</details>

---

**Câu 6.** (Khó) SNR lý thuyết của audio 12-bit xấp xỉ bao nhiêu dB?
- A. ≈ 72 dB
- B. ≈ 12 dB
- C. ≈ 96 dB
- D. ≈ 144 dB

<details><summary>Đáp án</summary>

**A.** `SNR ≈ 6.02 × bit = 6.02 × 12 ≈ 72 dB`. Bẫy C: 16-bit (~96 dB); bẫy D: 24-bit (~144 dB); bẫy B: nhầm "12 bit → 12 dB".
</details>

---

**Câu 7.** (Cực khó) Chuyển file 48 kHz / 24-bit / stereo sang 16 kHz / 16-bit / mono. Dung lượng (không nén) giảm bao nhiêu lần?
- A. ≈ 9 lần
- B. ≈ 3 lần
- C. ≈ 6 lần
- D. ≈ 4.5 lần

<details><summary>Đáp án</summary>

**A.** Tỉ lệ = (sample rate)×(channels)×(bit depth) = `(48/16) × (2/1) × (24/16) = 3 × 2 × 1.5 = 9`. Bẫy B: chỉ hạ sample rate; bẫy D: bỏ qua stereo→mono; bẫy C: bỏ qua đổi bit depth.
</details>

---

**Câu 8.** (Cực khó) Trích đặc trưng trên 2 giây audio 16 kHz, frame 25 ms, hop 10 ms. Số frame?
- A. 198 frame
- B. 200 frame
- C. 80 frame
- D. 320 frame

<details><summary>Đáp án</summary>

**A.** N_mẫu = 2 × 16000 = 32000; frame_len = 400 mẫu, hop = 160 mẫu. `⌊(32000 − 400)/160⌋ + 1 = ⌊197.5⌋ + 1 = 198`. Bẫy B: "2000ms/10ms = 200" (quên frame cuối không đủ chỗ).
</details>

---

## §2 — Ngữ âm & Âm học

**Câu 9.** (Khó) Waveform có 15 chu kỳ trong 0.05 giây. F0?
- A. 300 Hz
- B. 30 Hz
- C. 0.75 Hz
- D. 750 Hz

<details><summary>Đáp án</summary>

**A.** `F0 = 15 / 0.05 = 300 Hz`. Bẫy C: nhân thay vì chia (15 × 0.05); bẫy B: chia nhầm 10×.
</details>

---

**Câu 10.** (Cực khó) Chu kỳ dao động dây thanh 8 ms. F0 và hoạ âm bậc 4?
- A. F0 = 125 Hz; harmonic 4 = 500 Hz
- B. F0 = 8 Hz; harmonic 4 = 32 Hz
- C. F0 = 125 Hz; harmonic 4 = 31.25 Hz
- D. F0 = 1250 Hz; harmonic 4 = 5000 Hz

<details><summary>Đáp án</summary>

**A.** `F0 = 1/T = 1/0.008 = 125 Hz`; harmonic 4 = `4 × 125 = 500 Hz`. Bẫy C: **chia** F0 cho 4 (harmonic là **bội số**); bẫy D: quên đổi ms→s.
</details>

---

**Câu 11.** (Khó) Cường độ (intensity) âm A gấp 1000 lần âm B. Chênh mức bao nhiêu dB?
- A. 30 dB
- B. 1000 dB
- C. 3 dB
- D. 60 dB

<details><summary>Đáp án</summary>

**A.** `ΔL = 10·log₁₀(1000) = 10 × 3 = 30 dB`. Với **intensity** dùng hệ số **10**. Bẫy D: dùng hệ số 20 (dành cho amplitude/áp suất); bẫy B: quên log.
</details>

---

**Câu 12.** (Cực khó) **Biên độ** (amplitude) sóng tăng gấp 4 lần. Chênh mức bao nhiêu dB?
- A. ≈ 12.04 dB
- B. ≈ 6.02 dB
- C. ≈ 4 dB
- D. ≈ 40 dB

<details><summary>Đáp án</summary>

**A.** Với **amplitude** dùng hệ số **20**: `ΔL = 20·log₁₀(4) = 20 × 0.602 ≈ 12.04 dB`. Bẫy B: dùng hệ số 10 (nhầm với intensity) → 6.02. So sánh với Câu 11 để nhớ: **intensity → 10·log**, **amplitude → 20·log** (vì I ∝ A²).
</details>

---

**Câu 13.** (Cực khó) F0 = 150 Hz. Hoạ âm nào gần 1000 Hz nhất?
- A. Harmonic 7 (1050 Hz)
- B. Harmonic 6 (900 Hz)
- C. Harmonic 10 (1500 Hz)
- D. Harmonic 5 (750 Hz)

<details><summary>Đáp án</summary>

**A.** `1000/150 ≈ 6.67`. Harmonic 6 = 900 Hz (lệch 100), harmonic 7 = 1050 Hz (lệch **50**) → gần hơn. Harmonic là bội số nguyên của F0, không có harmonic đúng 1000 Hz.
</details>

---

## §3 — ASR & Đánh giá

**Câu 14.** (Khó) Reference 10 từ; hệ ASR mắc 2 substitutions, 1 deletion, 1 insertion. WER?
- A. 0.4
- B. 0.3
- C. 0.25
- D. 0.35

<details><summary>Đáp án</summary>

**A.** `WER = (S+D+I)/N = (2+1+1)/10 = 0.4`. Bẫy B: quên insertion (3/10). Nhớ mẫu số là **N reference**.
</details>

---

**Câu 15.** (Cực khó) Ref: "the cat sat on the mat" (6 từ). Hyp: "a cat sat on mat" (5 từ). Tính S, D, I và WER.
- A. S=1, D=1, I=0 → WER = 2/6 ≈ 0.333
- B. S=1, D=0, I=0 → WER = 1/6 ≈ 0.167
- C. S=0, D=1, I=1 → WER = 2/5 = 0.4
- D. S=2, D=1, I=0 → WER = 3/6 = 0.5

<details><summary>Đáp án</summary>

**A.** Căn chỉnh: the→**a** (S=1), cat=cat, sat=sat, on=on, the(thứ 2)→**xoá** (D=1), mat=mat. Vậy S=1, D=1, I=0 → `WER = 2/6 ≈ 0.333`. Bẫy C: chia cho số từ **hyp** (5). Bẫy: bỏ sót "the" thứ hai bị deletion.
</details>

---

**Câu 16.** (Khó) Một hệ ASR có WER = 15%. Word Accuracy là bao nhiêu?
- A. 85%
- B. 15%
- C. 115%
- D. 7.5%

<details><summary>Đáp án</summary>

**A.** `WAcc = 1 − WER = 1 − 0.15 = 0.85 = 85%`. Lưu ý: khi có nhiều insertion, WER > 100% ⇒ WAcc có thể **âm** (Accuracy không chặn ở 0).
</details>

---

**Câu 17.** (Khó) Hệ TTS tổng hợp 30 giây audio mất 6 giây tính toán. RTF và hệ nhanh gấp mấy lần real-time?
- A. RTF = 0.2; nhanh 5× real-time
- B. RTF = 5.0; chậm 5× real-time
- C. RTF = 0.2; đúng bằng real-time
- D. RTF = 0.05; nhanh 20× real-time

<details><summary>Đáp án</summary>

**A.** `RTF = t_xử_lý / t_audio = 6/30 = 0.2` → < 1 = nhanh hơn real-time; `1/0.2 = 5×`. Bẫy B: đảo tử/mẫu số.
</details>

---

**Câu 18.** (Cực khó) Đánh giá corpus 3 câu: tổng (S+D+I) = 30 lỗi, tổng số từ reference của 3 câu = 300. WER cấp corpus (micro) là bao nhiêu?
- A. 10%
- B. 30%
- C. 100%
- D. tuỳ trung bình cộng WER từng câu

<details><summary>Đáp án</summary>

**A.** WER chuẩn báo cáo là **micro**: `Σ(S+D+I) / ΣN = 30/300 = 0.10 = 10%`. **KHÔNG** lấy trung bình cộng WER từng câu (macro) vì câu ngắn bị trọng số quá lớn → con số khác và lệch (nên D là cách sai chuẩn).
</details>

---

**Câu 19.** (Cực khó) Một language model đạt cross-entropy 3 bit/từ trên tập test. Perplexity bằng bao nhiêu?
- A. 8
- B. 3
- C. 9
- D. 2

<details><summary>Đáp án</summary>

**A.** `Perplexity = 2^(cross-entropy tính bằng bit) = 2³ = 8`. Perplexity ~ "số lựa chọn trung bình" LM phân vân mỗi bước; thấp = LM tốt. Bẫy: nhầm PP = cross-entropy (3) hoặc 3² = 9.
</details>

---

## §4 — Tổng hợp & Bẫy đơn vị

**Câu 20.** (Cực khó) File 5 phút, 44.1 kHz, mono, biên độ lượng tử hoá thành 1024 mức. Kích thước tính theo **megabit (Mb)** và **megabyte (MB)** lần lượt là?
- A. ≈ 132.3 Mb ≈ 16.54 MB
- B. ≈ 132.3 MB ≈ 16.54 Mb
- C. ≈ 1058 Mb ≈ 132.3 MB
- D. ≈ 132.3 Mb ≈ 132.3 MB

<details><summary>Đáp án</summary>

**A.** 1024 mức = 2¹⁰ → **10 bit/mẫu**. `44100 × 10 × 300 = 132 300 000 bit = 132.3 Mb`; `÷8 = 16 537 500 byte ≈ 16.54 MB`. Bẫy chính: **lẫn Mb (megabit) với MB (megabyte)** — chênh nhau 8 lần (D coi hai đơn vị bằng nhau).
</details>

---

**Câu 21.** (Cực khó) File 48 kHz, 16-bit, stereo, dài 2 phút. Tính (a) kích thước không nén và (b) bit rate.
- A. (a) ≈ 23.04 MB; (b) 1536 kbps
- B. (a) ≈ 184.3 MB; (b) 1536 kbps
- C. (a) ≈ 23.04 MB; (b) 768 kbps
- D. (a) ≈ 11.52 MB; (b) 1536 kbps

<details><summary>Đáp án</summary>

**A.** Bit rate = `48000 × 16 × 2 = 1 536 000 bps = 1536 kbps`. Size = `1 536 000 × 120 s = 184 320 000 bit ÷ 8 = 23 040 000 byte ≈ 23.04 MB`. Bẫy B: quên ÷8; bẫy C: quên ×2 kênh trong bit rate; bẫy D: dùng mono cho size.
</details>

---

**Câu 22.** (Cực khó) Chuẩn hoá dữ liệu: hạ từ 44.1 kHz xuống 16 kHz (giữ nguyên bit depth & số kênh). Phần trăm dung lượng **tiết kiệm** được xấp xỉ bao nhiêu?
- A. ≈ 63.7%
- B. ≈ 36.3%
- C. ≈ 50%
- D. ≈ 2.76%

<details><summary>Đáp án</summary>

**A.** Kích thước tỉ lệ thuận sample rate: tỉ lệ giữ lại = `16000/44100 ≈ 0.363` → **tiết kiệm ≈ 1 − 0.363 = 0.637 = 63.7%**. Bẫy B: nhầm "phần giữ lại" thành "phần tiết kiệm"; bẫy D: lấy tỉ số 44.1/16 = 2.76 rồi quên đổi thành phần trăm.
</details>

---

### Bảng ánh xạ ôn tập
| Dạng bài | Câu | Ôn thêm |
|---|---|---|
| File size / bit rate | 1, 2, 3, 21 | [D-DSP](../on_tap/D-xu-ly-tin-hieu.md) |
| Bit depth ↔ mức, SNR | 4, 6 | [D-DSP](../on_tap/D-xu-ly-tin-hieu.md) |
| Nyquist / aliasing | 5 | [D-DSP](../on_tap/D-xu-ly-tin-hieu.md) |
| Resample / tiết kiệm | 7, 22 | [E-dữ-liệu](../on_tap/E-du-lieu.md) |
| Frame count (đặc trưng) | 8 | [H-ASR](../on_tap/H-nhan-dang-tieng-noi.md) |
| F0 / harmonic / dB | 9–13 | [B-ngữ-âm](../on_tap/B-ngu-am-hoc.md) |
| WER / WAcc / edit distance | 14, 15, 16, 18 | [F-đánh-giá](../on_tap/F-danh-gia.md) |
| RTF / perplexity | 17, 19 | [F-đánh-giá](../on_tap/F-danh-gia.md) |
| Bẫy đơn vị (Mb/MB, ÷8) | 20, 21 | [ONE-PAGER](../on_tap/00-ONE-PAGER.md) |

Sai ≥ 2 câu cùng dạng → quay lại file on_tap tương ứng và luyện lại nhóm đó.
