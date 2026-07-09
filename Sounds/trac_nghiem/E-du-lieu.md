# TRẮC NGHIỆM — Cụm E: Dữ liệu Tiếng nói (20 câu)
Nguồn: `04 - Dataset` + kinh nghiệm xây dữ liệu thực tế. Ôn kèm [E-dữ-liệu](../on_tap/E-du-lieu.md) và [playbook thực chiến](../on_tap/I-thuc-hanh-kinh-nghiem.md).

> **Cách dùng:** Phương án dài bằng nhau, không tô đậm. **(Nhiều đáp án)** = chọn đủ. **(Khó)/(Cực khó)** = phân biệt bẫy/suy luận sâu. Câu 16–20 nâng cao (leakage, chọn augmentation, SNR, rủi ro pseudo-label).

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

---

**Câu 16.** (Cực khó) Xây tập test cho ASR, một kỹ sư chia ngẫu nhiên theo câu (utterance) nên cùng một người nói xuất hiện ở cả train và test. Hệ quả nghiêm trọng nhất là gì?
- A. Speaker leakage → WER test lạc quan giả (model học "khớp giọng" quen), không phản ánh khả năng tổng quát; phải split **theo speaker**
- B. Không ảnh hưởng gì vì nội dung câu khác nhau là đủ
- C. Làm tăng WER test một cách giả tạo khiến model trông tệ hơn
- D. Chỉ ảnh hưởng tốc độ train, không ảnh hưởng độ chính xác đo được

<details><summary>Đáp án</summary>

**A.** Cùng speaker ở train+test → model đã "quen giọng" → **WER thấp giả** (optimistic bias), sụp đổ khi gặp giọng mới. Nguyên tắc: **split theo speaker** (và theo phiên/điều kiện thu) để test đo đúng generalization. Tương tự phải chống trùng lặp nội dung (text overlap). B, C, D hiểu sai hướng và mức độ.
</details>

---

**Câu 17.** (Khó) Chọn augmentation theo bài toán: phương án nào hợp lý nhất?
- A. ASR chống nhiễu/xa mic → thêm noise + RIR + SpecAugment; Speaker verification → cẩn trọng với pitch/speed vì có thể phá đặc trưng giọng
- B. Mọi bài toán speech đều nên dùng đúng một bộ augmentation giống hệt nhau
- C. Speaker verification nên speed-perturb mạnh để đổi cao độ giọng cho đa dạng
- D. ASR không bao giờ dùng augmentation vì làm sai transcript

<details><summary>Đáp án</summary>

**A.** Augmentation phải **khớp bất biến của bài toán**: ASR cần bất biến với nhiễu/phòng/che phổ → noise, RIR, SpecAugment tốt. Nhưng **speaker verification** dựa vào chính đặc trưng giọng (pitch, formant) → speed/pitch perturb mạnh có thể **xoá tín hiệu cần học** (C sai). D sai (ASR dùng augmentation rất nhiều, nhãn text không đổi khi thêm nhiễu/che phổ).
</details>

---

**Câu 18.** (Khó) VAD/silence trimming quá "mạnh tay" có rủi ro gì cần cân nhắc?
- A. Cắt nhầm phụ âm yếu/âm cuối nhẹ hoặc khoảng ngừng mang nghĩa (prosody) → hỏng transcript alignment và ngữ điệu
- B. Không có rủi ro, cắt càng nhiều lặng càng tốt cho mọi trường hợp
- C. Làm tăng kích thước file nên tốn lưu trữ
- D. Chỉ ảnh hưởng TTS, không bao giờ ảnh hưởng ASR

<details><summary>Đáp án</summary>

**A.** VAD quá nhạy có thể cắt **phụ âm vô thanh yếu** (/f/, /s/ nhỏ), **âm cuối nhẹ**, hoặc **pause có nghĩa** (ranh giới câu, nhấn) → sai biên giới, hỏng prosody. Phải chỉnh ngưỡng + margin. B sai (đánh đổi thật), C ngược (trim làm **nhỏ** file), D sai (ảnh hưởng cả ASR).
</details>

---

**Câu 19.** (Cực khó) Một đoạn thu có công suất tín hiệu (speech) = 400 đơn vị, công suất nhiễu nền = 4 đơn vị. SNR theo dB là bao nhiêu?
- A. 20 dB
- B. 100 dB
- C. 2 dB
- D. 40 dB

<details><summary>Đáp án</summary>

**A.** `SNR = 10·log₁₀(P_signal/P_noise) = 10·log₁₀(400/4) = 10·log₁₀(100) = 20 dB`. Với **power** dùng hệ số 10 (không phải 20 của amplitude). SNR ~20 dB là "khá sạch" cho ASR. Bẫy C: quên log (100 → nhầm ra nhỏ); bẫy D: dùng hệ số 20 của biên độ.
</details>

---

**Câu 20.** (Khó) Pseudo-labeling (self-training) có rủi ro cố hữu nào và cách giảm thiểu?
- A. Confirmation bias — model tự củng cố lỗi của chính nó; giảm bằng lọc theo confidence, dùng teacher mạnh hơn, và trộn dữ liệu có nhãn thật
- B. Không có rủi ro vì nhãn do model sinh luôn chính xác
- C. Làm mất toàn bộ dữ liệu có nhãn ban đầu
- D. Chỉ dùng được khi đã có 100% dữ liệu gán nhãn tay

<details><summary>Đáp án</summary>

**A.** Model gán nhãn cho chính mình → nếu sai, **lỗi được khuếch đại** qua các vòng (confirmation bias). Giảm thiểu: **lọc confidence cao**, dùng **teacher lớn hơn** (VD Whisper sinh weak label), giữ tỉ lệ **dữ liệu nhãn thật**, và kiểm tra trên tập vàng. B sai (nhãn không hoàn hảo); D mâu thuẫn mục đích (pseudo-label dùng khi **thiếu** nhãn).
</details>
