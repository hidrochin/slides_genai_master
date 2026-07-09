# TRẮC NGHIỆM — Cụm F: Đánh giá Mô hình Tiếng nói (16 câu)
Nguồn: `05 - Model Evaluation`. Ôn kèm [F-đánh-giá](../on_tap/F-danh-gia.md).

> **Cách dùng:** Phương án dài bằng nhau, không tô đậm. **(Nhiều đáp án)** = chọn đủ. **(Khó)** = tính toán/phân biệt bẫy. Nhớ: `WER = (S+D+I)/N`, `RTF = t_synth / t_audio`, `EER: FAR=FRR`.

---

**Câu 1.** Công thức Word Error Rate (WER) là gì?
- A. WER = (S + D + I) / N, với N là tổng số từ trong câu reference
- B. WER = (S + D + I) / N, với N là tổng số từ trong câu ASR xuất ra
- C. WER = (S + D + I) × N
- D. WER = (S − D − I) / N

<details><summary>Đáp án</summary>

**A.** WER = (Substitutions + Deletions + Insertions) / **N (số từ reference)**. Bẫy B: mẫu số là số từ **reference**, KHÔNG phải câu ASR. C, D sai phép toán.
</details>

---

**Câu 2.** (Khó) Reference: "Tôi thích ăn phở gà" (5 từ). ASR: "Tôi yêu ăn gà bò". WER bằng bao nhiêu?
- A. 0.6
- B. 0.4
- C. 0.2
- D. 1.0

<details><summary>Đáp án</summary>

**A.** "thích"→"yêu" (S=1), "phở" mất (D=1), "bò" thêm (I=1); N=5. `WER = (1+1+1)/5 = 0.6`. Bẫy: bỏ sót insertion "bò", hoặc quên phở bị deletion → ra 0.4/0.2.
</details>

---

**Câu 3.** (Nhiều đáp án) Đâu là các biến thể của WER được nêu?
- A. CER (Character Error Rate)
- B. SylER (Syllable Error Rate)
- C. PER (Phoneme Error Rate)
- D. SER (Sentence Error Rate)
- E. RTF (Real-Time Factor)

<details><summary>Đáp án</summary>

**A, B, C, D.** Bốn biến thể theo mức đơn vị: ký tự/âm tiết/âm vị/câu. **RTF** là metric **tốc độ** (thời gian tổng hợp / thời lượng), không phải biến thể error rate.
</details>

---

**Câu 4.** Word Accuracy (WAcc) liên hệ với WER như thế nào?
- A. WAcc = 1 − WER
- B. WAcc = 1 + WER
- C. WAcc = WER / 2
- D. WAcc = 1 / WER

<details><summary>Đáp án</summary>

**A.** `WAcc = 1 − WER`. VD WER 0.6 → WAcc 0.4 (40%).
</details>

---

**Câu 5.** (Khó) Vì sao accuracy/F1-score truyền thống không đủ để đánh giá mô hình tiếng nói?
- A. Vì chúng mất thông tin thời gian và không bắt được lỗi alignment — vốn quan trọng với ASR/TTS
- B. Vì chúng chỉ tính được trên dữ liệu train, không dùng cho test
- C. Vì speech không phải bài toán phân loại nên không có accuracy
- D. Vì accuracy luôn bằng 100% với mọi mô hình tiếng nói

<details><summary>Đáp án</summary>

**A.** Speech là chuỗi phụ thuộc **thời gian**; accuracy/F1 **không bắt lỗi alignment** (thứ tự, chèn/xoá), vốn cốt lõi với ASR/TTS. Đó là lý do dùng WER (có S/D/I) thay vì accuracy đơn thuần.
</details>

---

**Câu 6.** (Khó) Phân biệt 4 loại MOS. Phát biểu nào ĐÚNG?
- A. MOS = "tốt cỡ nào"; DMOS = "xuống cấp cỡ nào so với gốc"; CMOS = "A hay B tốt hơn"; SMOS = "có giống style/speaker không"
- B. MOS = "A hay B tốt hơn"; CMOS = "tốt cỡ nào"; DMOS = "giống speaker không"; SMOS = "xuống cấp cỡ nào"
- C. Cả bốn đều đo cùng một thứ, chỉ khác thang điểm
- D. DMOS và CMOS đều dùng thang 1-5 tuyệt đối

<details><summary>Đáp án</summary>

**A.** **MOS** (chất lượng tuyệt đối 1-5), **DMOS** (mức xuống cấp so reference), **CMOS** (so sánh A/B, thang **−3..+3**), **SMOS** (style/speaker similarity). D sai: CMOS dùng thang **−3..+3** (tương đối), không phải 1-5.
</details>

---

**Câu 7.** Thang điểm của CMOS (Comparative MOS) là gì?
- A. Từ −3 (B tốt hơn A nhiều) đến +3 (A tốt hơn B nhiều), 0 = không thiên vị
- B. Từ 1 (bad) đến 5 (excellent)
- C. Từ 0 đến 100%
- D. Từ −1 đến +1

<details><summary>Đáp án</summary>

**A.** CMOS thang **−3 … +3**, đo **preference tương đối** giữa hai hệ (A/B test). Thang 1-5 là của **MOS/DMOS** (bẫy B).
</details>

---

**Câu 8.** (Nhiều đáp án) Đâu là các metric ĐÁNH GIÁ KHÁCH QUAN (objective) cho TTS?
- A. Mel Cepstral Distortion (MCD)
- B. Real-Time Factor (RTF)
- C. Speaker Similarity (cosine/euclidean)
- D. MOS
- E. CMOS

<details><summary>Đáp án</summary>

**A, B, C.** Objective = tự động, tính được: MCD, RTF, Speaker Similarity. **MOS, CMOS, SMOS** là **subjective** (dựa tri giác người nghe).
</details>

---

**Câu 9.** MCD (Mel Cepstral Distortion): giá trị thế nào là tốt?
- A. MCD càng thấp càng tốt (khoảng cách nhỏ giữa mel-cepstral của audio thật vs tổng hợp)
- B. MCD càng cao càng tốt
- C. MCD = 1 là hoàn hảo
- D. MCD không liên quan chất lượng audio

<details><summary>Đáp án</summary>

**A.** MCD đo **khoảng cách** giữa mel-cepstral coefficients thật vs synthetic → **thấp = tốt hơn** (thường Euclidean hoặc DTW, setup parallel có ground-truth).
</details>

---

**Câu 10.** (Khó) Hệ TTS tổng hợp 4 giây audio trong 2 giây tính toán. RTF bằng bao nhiêu và ý nghĩa?
- A. RTF = 0.5 — nhanh gấp 2× real-time
- B. RTF = 2.0 — chậm gấp 2× real-time
- C. RTF = 0.5 — chậm hơn real-time
- D. RTF = 8.0 — nhanh hơn real-time

<details><summary>Đáp án</summary>

**A.** `RTF = t_tổng_hợp / t_audio = 2/4 = 0.5`. **RTF < 1 = nhanh hơn real-time** (0.5 nghĩa là 2× real-time). Bẫy B: đảo tử/mẫu số.
</details>

---

**Câu 11.** SUS (Semantically Unpredictable Sentences) dùng để làm gì trong test intelligibility?
- A. Tối thiểu ngữ cảnh ngữ nghĩa, buộc người nghe dựa thuần vào acoustic-phonetic cue
- B. Tối đa ngữ cảnh để người nghe đoán từ dễ hơn
- C. Đo tốc độ tổng hợp của hệ thống
- D. Kiểm tra kích thước file audio đầu ra

<details><summary>Đáp án</summary>

**A.** SUS (VD "The green snake liked a singing pencil") **tối thiểu ngữ cảnh ngữ nghĩa** → cô lập độ rõ articulation khỏi kiến thức ngôn ngữ trước, đo intelligibility "thuần". B ngược mục đích.
</details>

---

**Câu 12.** (Khó) Trong Speaker Similarity objective, quan hệ giữa Cosine Similarity và Euclidean Distance với "độ giống" là gì?
- A. Cosine cao (gần 1) = giống hơn; Euclidean thấp = giống hơn
- B. Cosine thấp = giống hơn; Euclidean cao = giống hơn
- C. Cả hai đều cao = giống hơn
- D. Cả hai đều thấp = giống hơn

<details><summary>Đáp án</summary>

**A.** **Cosine similarity** đo góc giữa embedding → gần **1 = giống hơn** (cao tốt). **Euclidean distance** đo khoảng cách → **thấp = giống hơn**. Đây là cặp dễ lẫn hướng.
</details>

---

**Câu 13.** (Khó) Trong Speaker Verification, EER (Equal Error Rate) là gì?
- A. Điểm mà FAR (chấp nhận kẻ mạo danh) = FRR (từ chối người thật); EER thấp = hệ tốt hơn
- B. Điểm mà FAR = 0 và FRR = 100%
- C. Tỉ lệ nhận dạng đúng speaker trong N người
- D. Trung bình cộng của accuracy và top-k accuracy

<details><summary>Đáp án</summary>

**A.** **EER** = điểm cân bằng **FAR = FRR** (đánh đổi ngưỡng); **thấp = tốt hơn**. C là mô tả Identification (khác bài toán). Verification là 1-1, Identification là 1-N.
</details>

---

**Câu 14.** Speaker Identification khác Speaker Verification ở metric nào?
- A. Identification dùng Accuracy / Top-k accuracy (bài toán 1-N); Verification dùng EER (bài toán 1-1)
- B. Cả hai đều chỉ dùng EER
- C. Identification dùng WER, Verification dùng MOS
- D. Identification dùng RTF, Verification dùng MCD

<details><summary>Đáp án</summary>

**A.** **Identification** (là ai trong N) → **Accuracy, Top-k, Confusion Matrix**. **Verification** (đúng người claim không) → **EER (FAR=FRR)**. WER/MOS/RTF/MCD thuộc ASR/TTS.
</details>

---

**Câu 15.** (Nhiều đáp án) Đâu là các cân nhắc ĐẠO ĐỨC & BẢO MẬT trong voice cloning được nêu?
- A. Watermarking — nhúng tín hiệu không nghe được để đánh dấu nội dung tổng hợp
- B. Consent trước khi clone giọng một người
- C. Đánh dấu rõ nội dung AI-generated để tránh lừa dối
- D. Tăng bit depth để giọng clone giống hơn
- E. Forensic AI để phát hiện giọng đã clone

<details><summary>Đáp án</summary>

**A, B, C, E.** Bốn cân nhắc đúng (watermarking, consent, đánh dấu AI-generated, forensic detection) chống fraud/impersonation. D là kỹ thuật tín hiệu, không phải vấn đề đạo đức/bảo mật.
</details>

---

**Câu 16.** Cách chia tập dữ liệu đúng cho đánh giá mô hình là gì?
- A. Train (seen, học tham số), Dev/Validation (seen, tối ưu hyperparameter & error analysis), Test (unseen)
- B. Train (unseen), Dev (unseen), Test (seen)
- C. Chỉ cần Train và Test, không cần Dev
- D. Cả ba tập đều là dữ liệu đã thấy (seen)

<details><summary>Đáp án</summary>

**A.** Train & Dev là **seen** (Dev để tối ưu hyperparameter/error analysis), **Test là unseen** (đánh giá cuối, đo tổng quát hoá). B đảo ngược seen/unseen; D sai (test phải unseen).
</details>
