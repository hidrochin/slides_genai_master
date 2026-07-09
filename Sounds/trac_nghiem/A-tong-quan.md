# TRẮC NGHIỆM — Cụm A: Tổng quan Công nghệ Tiếng nói (16 câu)
Nguồn: `00 - Speech Technology`, `01 - Articulatory Phonetics` (Introduction) + góc nhìn hệ thống thực tế. Ôn kèm [A-tổng-quan](../on_tap/A-tong-quan.md) và [playbook thực chiến](../on_tap/I-thuc-hanh-kinh-nghiem.md).

> **Cách dùng:** Phương án viết **dài bằng nhau, không tô đậm** — không đoán được đáp án qua hình thức. Tự chọn **trước**, rồi mở "Đáp án". Câu **(Nhiều đáp án)** có từ 2 phương án đúng — phải chọn ĐỦ mới tính đúng. Câu **(Khó)/(Cực khó)** đòi hỏi suy luận/phân biệt bẫy. Câu 13–16 nâng cao (SLU cascade vs E2E, độ khó của speech, anti-spoofing).

---

**Câu 1.** Công nghệ tiếng nói (Speech Technology) được mô tả nằm ở giao của những lĩnh vực nào? **(Nhiều đáp án)**
- A. Artificial Intelligence (Trí tuệ nhân tạo)
- B. Natural Language Processing (Xử lý ngôn ngữ tự nhiên)
- C. Human-Computer Interaction (Tương tác người-máy)
- D. Computer Graphics (Đồ hoạ máy tính)
- E. Operating Systems (Hệ điều hành)

<details><summary>Đáp án</summary>

**A, B, C.** Slide đặt Speech Technology ở giao của **AI + NLP + HCI**. Computer Graphics và Operating Systems không nằm trong bộ ba nền tảng được nêu. Lý do quan trọng của công nghệ tiếng nói cũng gắn với HCI (hiệu quả giao tiếp người-máy) và accessibility.
</details>

---

**Câu 2.** Đâu là khác biệt cốt lõi giữa **Speaker Recognition** và **Speech Recognition (ASR)**?
- A. Speaker Recognition xác định người đang nói là ai, còn ASR chuyển nội dung lời nói thành văn bản
- B. Speaker Recognition chuyển giọng thành văn bản, còn ASR xác định danh tính người nói
- C. Cả hai đều xác định danh tính người nói nhưng khác nhau về tốc độ xử lý
- D. Cả hai đều chuyển văn bản thành giọng nói nhưng khác nhau về chất lượng đầu ra

<details><summary>Đáp án</summary>

**A.** **Speaker** Recognition trả lời "**ai** đang nói" (danh tính), còn **Speech** Recognition/ASR trả lời "nói **gì**" (nội dung → văn bản). Đây là bẫy kinh điển do tên gọi gần giống. Phương án B đảo ngược, C và D sai bản chất cả hai tác vụ.
</details>

---

**Câu 3.** (Khó) Nối tác vụ với mô tả đúng: (1) Speaker Diarization, (2) Speaker Verification, (3) Speaker Identification.
- A. 1: xác minh 1-1; 2: "ai nói khi nào"; 3: xác định 1-N
- B. 1: "ai nói khi nào"; 2: xác minh 1-1; 3: xác định 1-N
- C. 1: xác định 1-N; 2: "ai nói khi nào"; 3: xác minh 1-1
- D. 1: "ai nói khi nào"; 2: xác định 1-N; 3: xác minh 1-1

<details><summary>Đáp án</summary>

**B.** **Diarization** = phân đoạn theo người nói ("who spoke when"), không nhất thiết biết danh tính. **Verification** = bài toán **1-1** (có đúng người được claim không → gắn với EER, xem [F](../on_tap/F-danh-gia.md)). **Identification** = bài toán **1-N** (là ai trong N người → Accuracy/Top-k). Phân biệt rõ để không lẫn ở cụm đánh giá.
</details>

---

**Câu 4.** MD&D (như ứng dụng ELSA Speak) là tác vụ nào?
- A. Mispronunciation Detection and Diagnosis — phát hiện và chẩn đoán lỗi phát âm
- B. Multi-Dialect Detection — phát hiện phương ngữ trong lời nói
- C. Music and Dialogue detection — tách nhạc khỏi hội thoại
- D. Model Debugging and Deployment — gỡ lỗi và triển khai mô hình

<details><summary>Đáp án</summary>

**A.** MD&D = **Mispronunciation Detection and Diagnosis** — không chỉ phát hiện phát âm sai mà còn **chẩn đoán** sai ở đâu, để phản hồi cho người học (ELSA Speak là ví dụ). Các phương án khác là bẫy chữ viết tắt.
</details>

---

**Câu 5.** Theo slide, tại sao hệ thống deep learning hiện đại "ít phụ thuộc vào việc mã hoá tri thức ngữ âm trực tiếp"?
- A. Vì để mô hình tự học ánh xạ chữ-âm từ dữ liệu thường tốt hơn thiết kế cấu trúc ngữ âm bằng tay
- B. Vì tri thức ngữ âm đã bị chứng minh là sai trong bối cảnh xử lý tiếng nói hiện đại
- C. Vì phần cứng hiện đại không đủ nhanh để chạy các quy tắc ngữ âm tường minh
- D. Vì ngữ âm học chỉ áp dụng cho tiếng Anh, không dùng được cho ngôn ngữ khác

<details><summary>Đáp án</summary>

**A.** Slide nêu: cho phép DL **học letter-sound mapping từ dữ liệu** thường tốt hơn hand-engineering cấu trúc ngữ âm. Nhưng lưu ý (bẫy ngược): ngữ âm học **vẫn hữu ích** để **mô tả & debug** hệ thống — không phải "sai" (B). C, D là suy diễn sai.
</details>

---

**Câu 6.** (Nhiều đáp án) Đâu là các thách thức của công nghệ tiếng nói được nêu, cùng giải pháp tương ứng đúng?
- A. Noise & Variability → Data augmentation
- B. Accents & Dialects → Thu dữ liệu đa dạng (VD Common Voice)
- C. Data Scarcity (low-resource) → Transfer learning + dữ liệu tổng hợp
- D. Ethical Concerns (deepfake) → Tăng bit depth khi thu âm
- E. Latency cao → Bỏ hoàn toàn Language Model

<details><summary>Đáp án</summary>

**A, B, C.** Ba cặp thách thức-giải pháp đúng theo slide. D sai: deepfake/riêng tư giải bằng **quy định + hướng dẫn đạo đức + watermarking**, không liên quan bit depth. E sai hoàn toàn (LM giúp cải thiện độ chính xác, xem [H](../on_tap/H-nhan-dang-tieng-noi.md)).
</details>

---

**Câu 7.** Ví dụ "Google đạt WER 5.1% trên Switchboard" minh hoạ cho điều gì?
- A. Hệ ASR hiện đại đã tiệm cận/ngang mức con người (~5-6%) trong điều kiện kiểm soát
- B. Con người luôn transcribe chính xác tuyệt đối 0% lỗi
- C. Switchboard là dataset TTS dùng để đo naturalness
- D. WER 5.1% nghĩa là hệ chỉ nhận đúng 5.1% số từ

<details><summary>Đáp án</summary>

**A.** Mốc con người ~5-6% WER; hệ đạt 5.1% ⇒ **ngang/tiệm cận con người**. B sai (con người vẫn có ~5-6% lỗi). C sai (Switchboard là hội thoại cho ASR). D hiểu ngược: WER 5.1% nghĩa là **tỉ lệ lỗi** 5.1%, tức nhận đúng ~94.9%.
</details>

---

**Câu 8.** Khác biệt chính giữa Rule-based AI và Machine Learning là gì?
- A. Rule-based dùng luật/logic do chuyên gia định nghĩa trước; ML học pattern từ dữ liệu lớn theo thời gian
- B. Rule-based học từ dữ liệu; ML dùng luật cứng do chuyên gia viết
- C. Cả hai đều học từ dữ liệu, chỉ khác kích thước mô hình
- D. Rule-based luôn chính xác hơn ML trong mọi bài toán tiếng nói

<details><summary>Đáp án</summary>

**A.** Rule-based = **predefined rules/logic by experts**; ML = **learns patterns from large datasets over time**. B đảo ngược. Deep Learning là nhánh của ML dùng mạng nhiều tầng, tự học đặc trưng.
</details>

---

**Câu 9.** (Nhiều đáp án) Đâu là các xu hướng hiện tại của công nghệ tiếng nói theo slide?
- A. On-device / real-time processing để bảo mật
- B. Multimodal (kết hợp speech + vision, VD lip-reading)
- C. Ethical AI (giảm bias, voice cloning có trách nhiệm)
- D. Quay lại hoàn toàn phương pháp template matching thập niên 1950
- E. End-to-end deep learning vượt phương pháp truyền thống

<details><summary>Đáp án</summary>

**A, B, C, E.** Bốn xu hướng đều được nêu (deep learning dominance, real-time on-device, multimodal, ethical AI). D sai: template matching là quá khứ, không phải xu hướng.
</details>

---

**Câu 10.** Ứng dụng "chẩn đoán Alzheimer qua speech patterns" thuộc lĩnh vực nào trong slide applications?
- A. Healthcare
- B. Entertainment
- C. Education
- D. Authentication

<details><summary>Đáp án</summary>

**A.** Slide xếp chẩn đoán Alzheimer qua giọng vào **Healthcare**. Education = công cụ học ngôn ngữ (TTS/ELSA); Entertainment = audiobook/lồng tiếng; Authentication = voice biometrics.
</details>

---

**Câu 11.** (Khó) Vì sao "voice biometrics" (VD Nuance) được xếp là ứng dụng, còn "Speaker Verification" được xếp là tác vụ?
- A. Voice biometrics là ứng dụng thực tế dựa trên tác vụ nền Speaker Verification/Identification
- B. Hai khái niệm hoàn toàn không liên quan nhau
- C. Voice biometrics chỉ dùng cho TTS, Speaker Verification chỉ dùng cho ASR
- D. Speaker Verification là ứng dụng, voice biometrics là tác vụ nghiên cứu

<details><summary>Đáp án</summary>

**A.** **Tác vụ** (task) là bài toán kỹ thuật (Speaker Verification/Identification); **ứng dụng** (application) là sản phẩm dùng tác vụ đó (voice biometrics xác thực khách hàng). Quan hệ nền tảng ↔ triển khai, không tách rời (B), không đảo vai (D), không giới hạn TTS/ASR (C).
</details>

---

**Câu 12.** Tầm nhìn (vision) tương lai của công nghệ tiếng nói theo slide là gì?
- A. Dân chủ hoá (democratizing) công nghệ tiếng nói — tiếp cận được và có đạo đức cho mọi người
- B. Chỉ phục vụ các tập đoàn công nghệ lớn để tối đa lợi nhuận
- C. Thay thế hoàn toàn giao tiếp bằng văn bản trong 2 năm tới
- D. Tập trung duy nhất vào tiếng Anh và loại bỏ ngôn ngữ ít tài nguyên

<details><summary>Đáp án</summary>

**A.** Vision: **democratizing speech technology — accessible and ethical for everyone**, kèm định hướng universal models, emotion recognition, low-power models cho vùng xa. D mâu thuẫn trực tiếp (định hướng ngược lại là hỗ trợ low-resource languages).
</details>

---

**Câu 13.** (Cực khó) Xây trợ lý giọng nói hiểu ý định người dùng (SLU) — so sánh kiến trúc cascade (ASR → NLU trên text) và E2E (audio → intent) đúng nhất là gì?
- A. Cascade tận dụng model ASR/NLU mạnh sẵn có & dễ debug nhưng lỗi ASR lan sang NLU; E2E giữ được ngữ điệu/paralinguistic và tránh error propagation nhưng cần nhiều dữ liệu audio-intent
- B. Cascade luôn tốt hơn E2E ở mọi mặt vì đơn giản hơn
- C. E2E không cần dữ liệu, cascade cần rất nhiều dữ liệu
- D. Hai kiến trúc giống hệt nhau, chỉ khác tên gọi

<details><summary>Đáp án</summary>

**A.** **Cascade** (ASR→NLU): dùng lại thành phần mạnh, dễ chèn LM & debug, nhưng **lỗi ASR trôi xuống** NLU và **mất thông tin âm thanh** (ngữ điệu, cảm xúc). **E2E**: giữ paralinguistic, không error propagation, nhưng **đói dữ liệu** (cặp audio↔intent hiếm) và khó debug. Chọn tuỳ tài nguyên dữ liệu & yêu cầu. B, C, D sai.
</details>

---

**Câu 14.** (Khó) Vì sao xử lý tiếng nói khó hơn xử lý văn bản thuần (text NLP)?
- A. Tín hiệu liên tục, biến thiên theo speaker/accent/tốc độ/nhiễu, không có ranh giới từ rõ, và có coarticulation (âm ảnh hưởng lẫn nhau)
- B. Vì text có nhiều ngôn ngữ hơn speech
- C. Vì speech luôn ngắn hơn text nên ít thông tin
- D. Vì text không cần model học còn speech thì cần

<details><summary>Đáp án</summary>

**A.** Speech là tín hiệu **liên tục, biến thiên cao** (cùng câu, hai người/hai lần nói ra rất khác), **không có khoảng trắng phân từ**, chịu **nhiễu & kênh thu**, và **coarticulation** (âm trước/sau nhoè vào nhau). Đây là gốc rễ khiến ASR/SLU khó hơn NLP text. B, C, D sai.
</details>

---

**Câu 15.** (Cực khó) Nối tác vụ với "hình dạng bài toán": (1) ASR, (2) Speaker Verification, (3) Speaker Identification, (4) SER (emotion).
- A. 1: seq2seq (audio→text); 2: nhị phân 1-1 (accept/reject); 3: phân loại 1-N; 4: phân loại nhãn cảm xúc
- B. 1: phân loại 1-N; 2: seq2seq; 3: nhị phân 1-1; 4: hồi quy RTF
- C. 1: nhị phân; 2: seq2seq; 3: seq2seq; 4: phân loại
- D. Cả bốn đều là bài toán seq2seq giống nhau

<details><summary>Đáp án</summary>

**A.** **ASR** = sequence-to-sequence (audio→chuỗi text). **Verification** = quyết định **nhị phân 1-1** (đúng người claim không → EER). **Identification** = **phân loại 1-N** (là ai → accuracy/top-k). **SER** = **phân loại** nhãn cảm xúc. Biết "hình dạng" giúp chọn loss & metric đúng. Các phương án khác gán sai.
</details>

---

**Câu 16.** (Khó) Anti-spoofing / phát hiện giọng giả (deepfake) trong hệ xác thực giọng thường dựa vào dấu hiệu nào?
- A. Artifact do vocoder/replay để lại (phân bố tần số bất thường, thiếu vi cấu trúc tự nhiên), dùng model countermeasure riêng cạnh speaker verification
- B. Chỉ cần tăng bit depth khi thu là loại được giọng giả
- C. Giọng giả luôn to hơn giọng thật nên đo âm lượng là đủ
- D. Không thể phát hiện được nên phải bỏ xác thực giọng

<details><summary>Đáp án</summary>

**A.** Giọng tổng hợp/replay để lại **artifact** (phổ bất thường, thiếu chi tiết vi mô, dấu vết vocoder) → hệ dùng **countermeasure/PAD** (Presentation Attack Detection) song song với speaker verification, đo bằng metric như **t-DCF/EER**. B, C, D là quan niệm sai; đây là mảng nghiên cứu tích cực (ASVspoof).
</details>
