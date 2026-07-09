# TRẮC NGHIỆM — Cụm E: Dữ liệu Tiếng nói (15 câu)
Nguồn: `04 - Dataset`. Ôn kèm [E-dữ-liệu](../on_tap/E-du-lieu.md).

> **Cách dùng:** Phương án dài bằng nhau, không tô đậm. **(Nhiều đáp án)** = chọn đủ. **(Khó)** = phân biệt bẫy.

---

**Câu 1.** (Nhiều đáp án) Đâu là các phương pháp thu thập dữ liệu tiếng nói được nêu?
- A. Studio recording
- B. Crowdsourced recording
- C. Crawling
- D. Synthesis (dùng TTS)
- E. Manual transcription từ sách in

<details><summary>Đáp án</summary>

**A, B, C, D.** Bốn phương pháp: studio, crowdsource, crawl, synthesis. E không phải phương pháp **thu thập audio** (transcription là gán nhãn, và từ sách in không tạo ra tiếng nói).
</details>

---

**Câu 2.** (Khó) Nối phương pháp với nhược điểm ĐẶC TRƯNG: (1) Studio, (2) Crowdsourced, (3) Crawling, (4) Synthesis.
- A. 1: ít đa dạng speaker & đắt; 2: chất lượng ghi âm không đều; 3: vấn đề bản quyền & transcript kém; 4: prosody thiếu tự nhiên & có thể tạo bias
- B. 1: bản quyền; 2: đắt; 3: prosody kém; 4: ít speaker
- C. 1: prosody kém; 2: bản quyền; 3: đắt; 4: ít speaker
- D. 1: chất lượng không đều; 2: đắt; 3: prosody kém; 4: bản quyền

<details><summary>Đáp án</summary>

**A.** Studio → đắt, ít đa dạng speaker (dù chất lượng cao). Crowdsource → chất lượng không đều, cần QC. Crawling → licensing/legal + transcript kém. Synthesis → prosody thiếu tự nhiên, có thể introduce bias, khó generalize. Các phương án khác xáo trộn sai.
</details>

---

**Câu 3.** Dataset nào KHÔNG phải dataset ASR theo phân loại trong slide?
- A. VoxCeleb
- B. LibriSpeech
- C. CommonVoice
- D. TEDLIUM

<details><summary>Đáp án</summary>

**A.** **VoxCeleb** là dataset **Speaker Recognition & Diarization**, không phải ASR. ASR: LibriSpeech, CommonVoice, TEDLIUM, VoxPopuli.
</details>

---

**Câu 4.** Kỹ thuật Pseudo Labeling gồm các bước theo thứ tự nào?
- A. Train model với dữ liệu có nhãn → dùng model dự đoán nhãn cho dữ liệu chưa nhãn → retrain với cả hai
- B. Dự đoán nhãn ngẫu nhiên → train → không cần dữ liệu có nhãn
- C. Thu thập nhãn thủ công toàn bộ → train một lần
- D. Train trên dữ liệu chưa nhãn trước → gán nhãn tay sau

<details><summary>Đáp án</summary>

**A.** Pseudo labeling: (1) train với **labeled data**, (2) model dự đoán **pseudo-label** cho unlabeled, (3) **retrain** với pseudo-labeled + labeled cùng nhau. Đây là dạng semi-supervised, cần dữ liệu có nhãn ban đầu (loại B).
</details>

---

**Câu 5.** Forced Alignment (căn chỉnh cưỡng bức) làm gì?
- A. Tự động căn chỉnh audio với transcription và xác định timestamp start/end của từ/phoneme
- B. Nén file audio để giảm kích thước
- C. Chuyển văn bản thành giọng nói
- D. Phân loại cảm xúc trong giọng nói

<details><summary>Đáp án</summary>

**A.** Forced alignment = align **audio ↔ transcription**, cho ra **timestamp chính xác** của word/phoneme. Phục vụ gán nhãn dataset ASR/TTS và phân tích ngữ âm/prosody.
</details>

---

**Câu 6.** (Khó) So sánh các phương pháp forced alignment: phát biểu nào ĐÚNG?
- A. HMM-GMM kém chính xác với speech tự nhiên do mô hình phoneme cứng nhắc; DL-based robust hơn với giọng/nhiễu nhưng tốn tài nguyên hơn
- B. E2E ASR-based (Whisper) chính xác nhất ở mức phoneme mịn
- C. CTC-based chậm hơn HMM và không xử lý được độ dài thay đổi
- D. HMM-GMM robust nhất với nhiễu và accent

<details><summary>Đáp án</summary>

**A.** HMM-GMM cứng nhắc → kém với spontaneous speech; DL-based (MFA) robust hơn nhưng nặng tính toán. B sai: E2E ASR **kém** chính xác ở mức phoneme mịn (dù tốt với speech tự nhiên/nhiễu). C sai: CTC **nhanh hơn** HMM và xử lý được độ dài linh hoạt. D sai (HMM-GMM là yếu nhất về robustness).
</details>

---

**Câu 7.** (Nhiều đáp án) Đâu là các bước tiền xử lý (Data Processing) tiếng nói được nêu?
- A. Speaker Diarization
- B. Silence Trimming
- C. Resampling (VD về 16 kHz cho ASR)
- D. Volume Normalization
- E. Tăng bit depth lên 64 bit để cải thiện nghĩa từ

<details><summary>Đáp án</summary>

**A, B, C, D.** Bốn bước đều được nêu (cùng Noise Reduction, Speech Segmentation). E là bịa — bit depth không liên quan tiền xử lý ngữ nghĩa, và 64 bit không phải chuẩn.
</details>

---

**Câu 8.** Tại sao cần Silence Trimming (cắt khoảng lặng)?
- A. Giảm kích thước & thời gian train, tránh frame lặng làm bias model, tăng độ phản hồi
- B. Tăng kích thước dataset để model học nhiều hơn
- C. Thêm nhiễu nền giúp model robust
- D. Chuyển đổi sample rate về chuẩn chung

<details><summary>Đáp án</summary>

**A.** Trim silence → nhỏ hơn, train nhanh hơn, **tránh frame lặng bias model**, model responsive hơn (VD 7s/660KB → 4s/400KB). B ngược hẳn; C là augmentation (mục đích khác); D là resampling.
</details>

---

**Câu 9.** VAD (Voice Activity Detection) dùng để làm gì?
- A. Phân biệt đoạn có tiếng nói (speech) với đoạn lặng/nhiễu (non-speech)
- B. Xác định danh tính người nói
- C. Đo chất lượng tín hiệu bằng SNR
- D. Chuyển giọng nói thành văn bản

<details><summary>Đáp án</summary>

**A.** VAD phân biệt **speech vs non-speech**, lọc lặng & nhiễu (bằng năng lượng hoặc ML) — dùng cho segmentation & silence trimming. B là speaker ID; D là ASR.
</details>

---

**Câu 10.** (Nhiều đáp án) Đâu là các kỹ thuật Speech Data Augmentation được nêu?
- A. Noise augmentation / room simulation (RIR)
- B. Speed perturbation (đổi tốc độ, giữ nguyên pitch)
- C. SpecAugment (masking spectrogram)
- D. Forced alignment
- E. Pseudo labeling

<details><summary>Đáp án</summary>

**A, B, C.** Ba kỹ thuật augmentation. D (forced alignment) và E (pseudo labeling) thuộc **gán nhãn/căn chỉnh**, không phải augment tín hiệu. Lưu ý speed perturbation **giữ nguyên pitch**.
</details>

---

**Câu 11.** (Khó) Trong pipeline Vietnam-Celeb, "face stream" được tạo bằng cách ghép các bounding box khuôn mặt liên tiếp thoả điều kiện gì?
- A. IoU (Intersection over Union) > 0.5
- B. SNR > 20 dB
- C. WER < 5%
- D. Cosine similarity > 0.9

<details><summary>Đáp án</summary>

**A.** Face stream = ghép bounding box liên tiếp có **IoU > 0.5** (S3FD detect). Sau đó ArcFace lấy embedding, K-means loại ảnh xấu, TalkNet xác minh người đang nói. SNR/WER/cosine là metric của bài toán khác.
</details>

---

**Câu 12.** Weak labels trong gán nhãn dữ liệu tiếng nói thường được tạo ra bằng cách nào?
- A. Sinh bởi mô hình lớn hơn cùng tác vụ (VD Whisper tự sinh transcript làm nhãn ASR)
- B. Do chuyên gia gán nhãn thủ công từng mẫu
- C. Lấy ngẫu nhiên từ từ điển
- D. Sao chép từ metadata của file audio

<details><summary>Đáp án</summary>

**A.** Weak labels thường do **mô hình lớn hơn cùng tác vụ** sinh (auto-transcription bằng Whisper, clustering cho speaker label, semi-supervised). Human annotation (B) chính xác hơn nhưng đắt — là hướng đối lập.
</details>

---

**Câu 13.** (Khó) Nối metric đánh giá chất lượng dataset với nhóm đúng: SNR, PESQ, STOI thuộc nhóm nào?
- A. Data Quality & Cleanliness
- B. Data Diversity & Representativeness
- C. Dataset Balance & Bias
- D. Labeling Accuracy

<details><summary>Đáp án</summary>

**A.** **SNR** (tỉ lệ tín hiệu/nhiễu, cao=tốt), **PESQ** (chất lượng theo tri giác), **STOI** (độ dễ hiểu trong nhiễu) đều đo **Quality & Cleanliness**. Diversity đo speaker/phonetic coverage; Balance đo gender/age/accent distribution; Labeling Accuracy đo IAA (Kappa).
</details>

---

**Câu 14.** Inter-Annotator Agreement (IAA) được đo bằng chỉ số nào?
- A. Cohen's Kappa, Fleiss' Kappa
- B. Word Error Rate
- C. Real-Time Factor
- D. Mel Cepstral Distortion

<details><summary>Đáp án</summary>

**A.** IAA đo mức đồng thuận giữa người gán nhãn → **Cohen's Kappa / Fleiss' Kappa**. WER/RTF/MCD là metric đánh giá **mô hình** (ASR/TTS), không phải agreement giữa annotator.
</details>

---

**Câu 15.** Xu hướng mới nào được nêu trong đánh giá chất lượng/nhãn dataset?
- A. LLM as a judge
- B. Quay lại gán nhãn thủ công 100%
- C. Bỏ hoàn toàn bước benchmark
- D. Chỉ dùng dữ liệu tổng hợp, loại bỏ dữ liệu thật

<details><summary>Đáp án</summary>

**A.** Slide nêu xu hướng **LLM as a judge** cho đánh giá nhãn/chất lượng. Các phương án còn lại đi ngược best practices (vẫn cần benchmark, human-in-the-loop, dữ liệu đa dạng).
</details>
