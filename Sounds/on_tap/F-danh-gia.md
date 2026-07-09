# F — Đánh giá Mô hình Tiếng nói (Model Evaluation)

> Nguồn: `05 - Model Evaluation`. Cụm NHIỀU CÔNG THỨC & METRIC: WER và biến thể, MOS/DMOS/CMOS/SMOS, MCD, RTF, speaker similarity, FAR/FRR/EER.

Điều hướng: [00-ONE-PAGER](00-ONE-PAGER.md) · [E-dữ-liệu](E-du-lieu.md) · [G-tổng-hợp](G-tong-hop-tieng-noi.md) · [H-nhận-dạng](H-nhan-dang-tieng-noi.md)

---

## 1. Vì sao đánh giá & tách tập dữ liệu

- Đánh giá = đo mô hình chạy tốt ra sao trên **dữ liệu chưa thấy (unseen)**; so sánh các mô hình.
- **Tách tập:**
  - **Train** — Seen (học tham số).
  - **Dev/Validation** — Seen (tối ưu **hyperparameter**, error analysis).
  - **Test** — **Unseen** (đánh giá cuối).
- Vì sao accuracy/F1 truyền thống **không đủ** cho speech: mất **thông tin thời gian (temporal)** — speech là chuỗi phụ thuộc thời gian; accuracy/F1 **không bắt lỗi alignment** (rất quan trọng cho ASR/TTS).

## 2. Metric theo tác vụ — BẢNG TỔNG HỢP HAY HỎI

| Tác vụ | Metric chính |
|---|---|
| **STT / ASR** | **WER**, SylER, CER, PER |
| **TTS** | **MOS**, Intelligibility (**WER**), **MCD** |
| **Voice Cloning** | Similarity Score, WER, MOS, SNR |
| **Voice Conversion** | Similarity Score, WER |
| **Speaker Verification** | **EER** (Equal Error Rate) |
| **Speaker Identification** | Accuracy, Top-k accuracy, Confusion Matrix |

## 3. WER (Word Error Rate) — CÔNG THỨC LÕI

```
WER = (S + D + I) / N
```
- **S** = Substitutions (thay sai), **D** = Deletions (bỏ sót), **I** = Insertions (thêm thừa).
- **N** = tổng số từ trong **reference** (câu chuẩn), KHÔNG phải câu ASR xuất ra.

### Ví dụ mẫu (bám slide):
- Reference: "Tôi thích ăn phở gà" (N = 5). ASR: "Tôi yêu ăn gà bò".
- "thích"→"yêu" = **S=1**; "phở" mất = **D=1**; "bò" thêm = **I=1**.
- WER = (1+1+1)/5 = **0.6 (60%)**.

**Biến thể WER:**
- **CER (Character Error Rate)** — mức ký tự (hợp ngôn ngữ chữ viết phức tạp).
- **SylER (Syllable Error Rate)** — mức âm tiết.
- **PER (Phoneme Error Rate)** — mức âm vị.
- **SER (Sentence Error Rate)** — % câu có **≥ 1 lỗi**.

**Ưu:** phổ biến, dễ tính, liên quan trực tiếp chất lượng ASR.
**Nhược:** không xét **ngữ nghĩa**; **phạt lỗi nhỏ bằng lỗi lớn**; nhạy với OOV & danh từ riêng.

**Metric ASR khác:**
- **Accuracy = (từ đúng / tổng từ) × 100%**; **WAcc = 1 − WER** (Word Accuracy).
- **WRR (Word Recognition Rate)** — tỉ lệ từ nhận đúng.
- **Latency (Time to Transcription)** — thời gian từ nhận audio đến ra text; quan trọng cho real-time (live caption).
- **Mốc tham chiếu:** con người ~**5–6%** WER; Google trên **Switchboard đạt WER 5.1%** (ngang người).

## 4. Đánh giá TTS / Voice Cloning

### 4.1 Phân loại metric
- **Objective (tự động, tính được):** **MCD**, Latency/**RTF**, Speaker Similarity.
- **Subjective (theo tri giác người):** **MOS, CMOS, SMOS**, ABX / A/B Test.
- **Intelligibility (độ dễ hiểu):** đo bằng **WER** (người nghe chép lại rồi so).

### 4.2 Họ MOS (Mean Opinion Score) — PHÂN BIỆT RÕ 4 LOẠI
- **MOS:** "Giọng này tốt thế nào?" — thang **1–5** (5 Excellent … 1 Bad), đánh giá naturalness/intelligibility. **Phải kèm ground-truth**. Tính: trung bình điểm mỗi mẫu rồi trung bình toàn hệ; báo thêm **SD** & **CI 95%**.
- **DMOS (Degradation MOS):** "So với bản gốc, xuống cấp bao nhiêu?" — so clean vs degraded, thang 1 (rất xuống cấp) → 5 (không xuống cấp). Dùng cho speech enhancement, denoising, codec, telecom/VoIP.
- **CMOS (Comparative MOS):** "A hay B tốt hơn?" — **so sánh tương đối**, thang **−3 … +3** (+3: A tốt hơn B nhiều; 0: không thiên vị; −3: B tốt hơn A nhiều). Dùng A/B test model vs baseline.
- **SMOS (Style/Speaker MOS):** "Có đúng speaker/cảm xúc/phong cách không?" — **Style MOS** (biểu cảm/intonation) & **Speaker MOS** (giống target speaker — cho voice cloning).

> Nhớ nhanh: **MOS**=tốt cỡ nào · **DMOS**=xuống cấp cỡ nào · **CMOS**=cái nào hơn · **SMOS**=có giống style/speaker không.

### 4.3 Perception Test & Intelligibility
- Loại test: MOS, ABX, AB, Intelligibility, DMOS, CMOS/SMOS, DCR (Degradation Category Rating), Preference Test.
- Mục tiêu: **Benchmarking** (so đối thủ/người thật), **Fine-tuning**, **User acceptance**.
- **Intelligibility qua WER:** cho người nghe **chép lại** speech tổng hợp rồi so ground truth.
- **SUS (Semantically Unpredictable Sentences):** câu **tối thiểu ngữ cảnh ngữ nghĩa** (VD "The green snake liked a singing pencil") → buộc nghe bằng **acoustic-phonetic cue thuần**, tách độ rõ articulation khỏi kiến thức ngôn ngữ trước.
- Lưu ý: listener fatigue (giữ test ngắn), vocabulary familiarity, reliability (nhiều rater & test lớn).

### 4.4 MCD & RTF — CÔNG THỨC
- **MCD (Mel Cepstral Distortion):** khoảng cách giữa **mel-cepstral coefficients** của audio thật vs tổng hợp. **MCD thấp = tốt hơn**. Thường dùng setup parallel có ground-truth (Euclidean hoặc DTW).
- **RTF (Real-Time Factor):**
  ```
  RTF = thời gian tổng hợp / thời lượng audio sinh ra
  ```
  **RTF < 1 = nhanh hơn real-time** (VD RTF 0.5 = nhanh gấp 2× real-time). Trade-off: tổng hợp nhanh có thể giảm chất lượng nếu model nhỏ/đơn giản; streaming/chunk giảm **perceived latency** nhưng có thể ảnh hưởng liên tục âm thanh. Nhớ báo **hardware** (CPU/GPU/RAM).

## 5. Voice Cloning — Speaker Similarity

- **Subjective:** MOS cho similarity, thang 1 (Not Similar) → 3 (Somewhat) → 5 (Very Similar); test randomized so original vs cloned.
- **Objective — Speaker Embedding Distance:**
  - **Cosine Similarity:** gần **1 = giống hơn** (cao = tốt).
  - **Euclidean Distance:** **thấp = giống hơn**.
- Cân bằng **speaker similarity ↔ intelligibility**: giọng clone rất tự nhiên nhưng **intelligibility thấp là có vấn đề**; lý tưởng WER gần với speaker gốc.
- **Đạo đức & bảo mật:** phát hiện giọng tổng hợp (human/AI); rủi ro fraud/misinformation/impersonation; **Watermarking** (nhúng tín hiệu không nghe được) & forensic AI; **consent trước khi clone**; đánh dấu rõ nội dung AI-generated.

## 6. Speaker Verification vs. Identification — DỄ NHẦM

### 6.1 Verification (1-1: đúng người claim không?)
- **FAR (False Acceptance Rate):** tỉ lệ **chấp nhận kẻ mạo danh** (false positive).
- **FRR (False Rejection Rate):** tỉ lệ **từ chối người thật** (false negative).
- **EER (Equal Error Rate):** điểm mà **FAR = FRR**. **EER thấp = hệ tốt hơn.**
- (Có sự đánh đổi: hạ ngưỡng → FAR tăng/FRR giảm và ngược lại; EER là điểm cân bằng.)

### 6.2 Identification (1-N: là ai trong N người?)
- **Accuracy = (số dự đoán đúng / tổng mẫu) × 100%**. VD 85/100 → 85%.
- **Top-k Accuracy:** speaker đúng có nằm trong **k ứng viên** dự đoán hàng đầu không.
- Dùng **Confusion Matrix** để phân tích lỗi.

## 7. Thách thức đánh giá & xu hướng

Cross-metric trade-off (cân bằng nhiều ưu tiên) · tính **chủ quan** của human judgment · **đạo đức** (bias & fairness) · xu hướng mới: **explainable AI (XAI)**, **multimodal evaluation**, **LLM as a judge**.
