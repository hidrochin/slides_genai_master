# Trắc nghiệm Chương 1 – Giới thiệu GenAI trong Tin sinh, Y học & CSSK

> ⚠️ **Multiple-select: mỗi câu có 0→nhiều đáp án đúng.** Xét **từng phương án như một câu Đúng/Sai độc lập**.
> 🎚️ Độ khó: 🟢 TB · 🟠 Khó · 🔴 Rất khó. Giải thích nằm trong khối **▸ Đáp án** ngay dưới mỗi câu (bấm để mở) — hãy tự làm trước khi mở.

---

### Câu 1 · 🟠 Khó
Phát biểu nào ĐÚNG về mô hình **discriminative** vs **generative**?
- A. Discriminative mô hình hóa `P(Y|X)`; generative mô hình hóa `P(X)` hoặc `P(X,Y)`
- B. Một mô hình generative **không thể** dùng để phân loại
- C. Có thể suy ra bộ phân loại từ generative qua định lý Bayes: `P(Y|X) ∝ P(X|Y)P(Y)`
- D. Generative luôn được huấn luyện **có giám sát**
- E. VAE và GAN là mô hình generative; hồi quy logistic là discriminative
- F. Chỉ generative mới lấy mẫu (sample) ra dữ liệu mới được

<details><summary>▸ Đáp án</summary>

**Đúng: A, C, E, F**

- ✅ **A** — định nghĩa chuẩn.
- ❌ **B** — sai: generative *có thể* phân loại (qua Bayes, xem C). Đây là bẫy "tuyệt đối".
- ✅ **C** — đúng, đây chính là cách generative làm classification.
- ❌ **D** — sai: generative thường **không giám sát** (học `P(X)`); có thể có điều kiện `P(X|Y)` nhưng không "luôn giám sát".
- ✅ **E** — ví dụ chuẩn.
- ✅ **F** — đúng: khả năng **sinh dữ liệu mới bằng lấy mẫu** là đặc trưng của generative (discriminative chỉ vẽ ranh giới).
</details>

---

### Câu 2 · 🔴 Rất khó
Về vai trò của **sinh dữ liệu nhân tạo** (artificial data) trong y sinh, phát biểu nào ĐÚNG?
- A. Giúp **data augmentation** cho quần thể thiếu dữ liệu
- B. Sinh genome nhân tạo **loại bỏ hoàn toàn** mọi rủi ro lộ danh tính
- C. Có thể hỗ trợ suy diễn khi **thiếu nhãn** (vd dự đoán biến thể gây bệnh không cần ClinVar)
- D. Bảo vệ quyền riêng tư bằng cách chia sẻ dữ liệu tổng hợp thay cho dữ liệu bệnh nhân thật
- E. Đảm bảo mô hình downstream đạt độ chính xác 100%
- F. Là một động lực chính để dùng **generative AI** thay vì chỉ discriminative

<details><summary>▸ Đáp án</summary>

**Đúng: A, C, D, F**

- ✅ **A, D, F** — đúng: 3 động lực kinh điển (augmentation, privacy, và bản chất sinh dữ liệu là của generative).
- ❌ **B** — sai: dữ liệu tổng hợp **giảm** rủi ro chứ không "loại bỏ hoàn toàn" (vẫn có nguy cơ overfit/rò rỉ mẫu — xem AATS ở Ch4). Bẫy "tuyệt đối".
- ✅ **C** — đúng: đây là lợi thế lớn (unsupervised inference).
- ❌ **E** — sai: không có gì đảm bảo 100%. Bẫy "tuyệt đối".
</details>

---

### Câu 3 · 🟠 Khó
Về xét nghiệm **NIPT**, chọn phát biểu ĐÚNG:
- A. Dựa trên **cfDNA của thai** lưu hành trong máu mẹ, giải trình tự để phát hiện lệch bội
- B. Là xét nghiệm **xâm lấn**, lấy mẫu trực tiếp mô thai
- C. Phát hiện Trisomy 21, 18, 13
- D. Là xét nghiệm **chẩn đoán xác định**, kết quả dương tính không cần xác nhận thêm
- E. Là xét nghiệm **sàng lọc** — dương tính vẫn cần xét nghiệm xâm lấn (chọc ối) khẳng định

<details><summary>▸ Đáp án</summary>

**Đúng: A, C, E**

- ✅ **A, C** — đúng bản chất & phạm vi phát hiện.
- ❌ **B** — sai: NIPT = **Non-Invasive** (không xâm lấn).
- ❌ **D** — sai: NIPT là **sàng lọc (screening)**, không phải chẩn đoán; dương tính cần khẳng định (E đúng). Đây là bẫy screening↔diagnostic (liên hệ Ch5).
- ✅ **E** — đúng.
</details>

---

### Câu 4 · 🔴 Rất khó
Về cơ chế **oncogene** vs **tumor suppressor**, phát biểu nào ĐÚNG?
- A. Oncogene gây ung thư qua **gain-of-function**; thường chỉ cần **một** allele bị kích hoạt
- B. Tumor suppressor gây ung thư qua **loss-of-function**; thường cần mất chức năng **cả hai** allele ("two-hit")
- C. TP53, RB1, PTEN, BRCA1/2 là oncogene
- D. KRAS "luôn bật" do đột biến hoạt hóa là ví dụ oncogene gain-of-function
- E. Vì BRCA là tumor suppressor nên **một** biến thể gây mất chức năng một copy là đủ gây ung thư ngay
- F. p53 bình thường khởi động apoptosis và sửa DNA lỗi

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, D, F**

- ✅ **A, B** — đúng, và là điểm phân biệt "khó": oncogene **1 hit** (trội ở mức tế bào), tumor suppressor **2 hit** (lặn ở mức tế bào).
- ❌ **C** — sai: TP53/RB1/PTEN/BRCA đều là **tumor suppressor**, không phải oncogene.
- ✅ **D, F** — đúng.
- ❌ **E** — sai: mất **một** copy tumor suppressor thường chưa đủ (cần two-hit); mang biến thể chỉ **tăng nguy cơ**, không gây ung thư "ngay". Bẫy hiểu sai cơ chế.
</details>

---

### Câu 5 · 🟠 Khó
Về khung **Disease–Gene–Drug** và các cách tiếp cận tính toán:
- A. 3 liên kết cần dự đoán: Drug–Target, Disease–Gene, Drug–Disease
- B. **Disease module principle**: gen liên quan bệnh giống nhau nằm gần nhau trong mạng sinh học → nền của network-based
- C. Do thiếu nhãn âm, ML hay dùng **PU learning** / bán giám sát
- D. Drug–Disease association chính là bài toán **drug repositioning**
- E. Data-mining-based **không** thuộc các cách tiếp cận được nêu
- F. Đối tượng (drug/gene/disease) có thể biểu diễn bằng structure, sequence, network, text

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đều đúng theo khung CBM.
- ❌ **E** — sai: 3 cách tiếp cận là **network-based, ML-based, data-mining-based** → data-mining CÓ thuộc.
</details>

---

### Câu 6 · 🟠 Khó
Ghép **Drug–Target Interaction** với ví dụ ĐÚNG:
- A. *1 thuốc – 1 đích*: Albuterol tác động thụ thể beta2AR (gen ADRB2)
- B. *Nhiều thuốc – 1 đích*: ZMapp = hỗn hợp **3 kháng thể đơn dòng** gắn protein virus Ebola
- C. *1 thuốc – nhiều đích*: Imatinib (trị CML, ALL)
- D. Imatinib là ví dụ *1 thuốc – 1 đích*
- E. ZMapp là **small molecule** đơn lẻ

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C**

- ✅ **A, B, C** — ghép đúng.
- ❌ **D** — sai: Imatinib là **đa đích** (1 thuốc – nhiều đích).
- ❌ **E** — sai: ZMapp là tổ hợp **kháng thể đơn dòng** (biologics), không phải small molecule đơn lẻ.
</details>

---

### Câu 7 · 🟠 Khó
Về **drug repositioning** (tái định vị thuốc), chọn phát biểu ĐÚNG:
- A. Ước tính ~**75%** thuốc *về lý thuyết* có thể được tái định vị
- B. Thuốc tái định vị có thể chiếm ~**30%** số thuốc được phê duyệt hằng năm
- C. "Known compound → target screening" nghĩa là biết hợp chất, đi tìm đích mới
- D. Repositioning bắt buộc phải phát triển phân tử hoàn toàn mới từ đầu
- E. Ebselen (vốn cho đột quỵ) từng được xét cho rối loạn lưỡng cực là ví dụ repositioning

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B** — số liệu "đắt" hay hỏi (75% và 30%).
- ✅ **C** — đúng một trong 3 mô hình phát triển thuốc.
- ❌ **D** — sai: bản chất repositioning là **dùng lại thuốc đã có**, không tạo mới từ đầu.
- ✅ **E** — đúng ví dụ.
</details>

---

### Câu 8 · 🟢 TB
Về nền tảng di truyền của bệnh và vi khuẩn kháng thuốc:
- A. Tỷ lệ bệnh di truyền tăng theo tuổi: ~5% sơ sinh → ~5% người lớn <25 → ~60% người già
- B. Bệnh có thể **đa gen (polygenic)**, không chỉ đơn gen
- C. Với chủng vi khuẩn đa kháng mới: cần dự đoán **kháng sinh nào còn nhạy**
- D. Cần đề xuất **cơ chế kháng thuốc mới** và **thuốc mới**
- E. Mục tiêu ML là **tạo ra** chủng kháng thuốc nguy hiểm hơn

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: mục tiêu là **chống** vi khuẩn, không tạo chủng nguy hiểm.
</details>

---

### Câu 9 · 🔴 Rất khó
Chọn **TẤT CẢ** phát biểu **SAI**:
- A. Discriminative học `P(X)` để sinh dữ liệu; generative học ranh giới quyết định
- B. NIPT là xét nghiệm chẩn đoán xác định, thay thế hoàn toàn chọc ối
- C. Oncogene cần "two-hit" (mất cả 2 allele) mới gây bệnh
- D. Precision oncology dựa vào phát hiện đột biến của bệnh nhân để chọn điều trị đích
- E. gnomAD/COSMIC là ví dụ nguồn dữ liệu dùng trong phân tích genomics

<details><summary>▸ Đáp án</summary>

**SAI: A, B, C** (D, E đúng)

- ❌ **A** — đảo ngược discriminative/generative.
- ❌ **B** — NIPT là **sàng lọc**, không thay thế chẩn đoán.
- ❌ **C** — "two-hit" là của **tumor suppressor**, không phải oncogene (oncogene chỉ cần 1 hit).
- ✅ **D, E** — đúng (đây là 2 phương án gài để bạn không chọn nhầm).
</details>

---

### Câu 10 · 🟢 TB
Về **Computational Biomedicine (CBM)**:
- A. Tích hợp dữ liệu đa tầng → xây CSDL lớn → khám phá tri thức mới
- B. Hỗ trợ **sàng lọc – chẩn đoán – điều trị** bệnh phức tạp
- C. Dùng phương pháp tính toán (AI, toán, thống kê) trên dữ liệu high-throughput
- D. Chỉ xử lý dữ liệu genomics, không dùng dữ liệu mạng/văn bản
- E. Đánh giá môn: Mid-term 50%, Final 50%

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B, C** — đúng định nghĩa CBM.
- ❌ **D** — sai: CBM tích hợp **nhiều loại** dữ liệu (structure, sequence, network, text...).
- ✅ **E** — đúng (chi tiết môn học).
</details>
