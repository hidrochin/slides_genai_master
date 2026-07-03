# Trắc nghiệm Chương 5 – Y học cá thể hóa (Personalized Medicine)

> ⚠️ **Multiple-select: mỗi câu có 0→nhiều đáp án đúng.** Xét **từng phương án như một câu Đúng/Sai độc lập**.
> 🎚️ Độ khó: 🟢 TB · 🟠 Khó · 🔴 Rất khó. Giải thích trong khối **▸ Đáp án** dưới mỗi câu — tự làm trước khi mở.

---

### Câu 1 · 🟠 Khó
Phân biệt **Precision / Pharmacogenomics / Personalized Medicine**:
- A. Precision/Stratified: chia bệnh nhân thành **nhóm** để điều trị phù hợp
- B. Pharmacogenomics (PGx): tối ưu liệu pháp dựa trên **genomics** của bệnh nhân (dự đoán đáp ứng & ADR)
- C. Personalized Medicine: tích hợp **đa -omics** của cá nhân
- D. Precision Medicine = dùng **cùng một** thuốc/liều cho **mọi** bệnh nhân
- E. PGx dựa trên **toàn bộ đa -omics** (proteomics, metabolomics...) chứ không chỉ genomics

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C**

- ✅ **A, B, C** — đúng.
- ❌ **D** — sai: precision = phân **nhóm** (đối lập với "cùng liều cho mọi người").
- ❌ **E** — sai: PGx dựa **chỉ genomics**; **Personalized** mới là đa -omics. Bẫy PGx↔Personalized.
</details>

---

### Câu 2 · 🔴 Rất khó
Ghép **-omics** ↔ đối tượng/định nghĩa:
- A. **Genomics** = DNA/gen ("blueprint")
- B. **Transcriptomics** = RNA — "**snapshot** biểu hiện gen tại 1 thời điểm"
- C. **Proteomics** = protein — "**functional output** của genome"
- D. **Metabolomics** = phân tử nhỏ (amino acid, đường, lipid, nucleotide, vitamin)
- E. Transcriptomics = metabolite; Proteomics = RNA
- F. Theo Central Dogma: DNA → RNA → Protein → Metabolite

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: đảo lộn đối tượng (transcriptomics = RNA, proteomics = protein).
</details>

---

### Câu 3 · 🔴 Rất khó
Về **GWAS** & Manhattan plot:
- A. So sánh genome **case (có bệnh)** vs **control (không bệnh)**
- B. Tìm biến thể xuất hiện **thường xuyên hơn** ở nhóm bệnh
- C. Trục Y của Manhattan plot là **−log₁₀(P-value)**; điểm càng **cao** = P càng nhỏ = càng có ý nghĩa
- D. **Cần** biết gene cụ thể mới ước lượng được nguy cơ
- E. Trục Y là **P-value** trực tiếp; điểm càng cao P càng lớn
- F. Có thể có hàng trăm–hàng nghìn biến thể liên quan một bệnh

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, F**

- ✅ **A, B, C, F** — đúng.
- ❌ **D** — sai: **không cần** biết gene cụ thể vẫn ước lượng nguy cơ (PRS cộng dồn nhiều biến thể).
- ❌ **E** — sai: trục Y là **−log(P)**, không phải P; điểm cao = P **nhỏ**. Bẫy đọc trục.
</details>

---

### Câu 4 · 🔴 Rất khó
Về **giới hạn của PRS** (câu tủ):
- A. PRS chỉ giải thích **nguy cơ tương đối (relative risk)**, không phải tuyệt đối
- B. PRS chỉ cho **tương quan**, không phải **nhân quả**
- C. PRS **không** tính yếu tố môi trường/lối sống
- D. Phần lớn dữ liệu từ người **gốc Âu** → có thể chỉ chính xác cho quần thể này
- E. Hai người cùng PRS thì chắc chắn khởi phát bệnh ở cùng độ tuổi
- F. PRS luôn cho kết quả **chắc chắn** (không phải xác suất)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng (4 giới hạn kinh điển).
- ❌ **E** — sai: PRS **không** cho biết mốc/thời gian tiến triển (22 tuổi vs 98 tuổi khác nhau).
- ❌ **F** — sai: PRS luôn là **xác suất**, không chắc chắn.
- 🎯 Câu có "chắc chắn / tuyệt đối / mọi chủng tộc / nhân quả" trong PRS thường **sai**.
</details>

---

### Câu 5 · 🟠 Khó
Phân biệt **absolute risk** vs **relative risk**:
- A. **Absolute risk**: khả năng bệnh xảy ra thực sự (vd BRCA1 → 60–80% ung thư vú)
- B. **Relative risk**: so nguy cơ với một nhóm tham chiếu khác
- C. PRS cho **relative risk**, không phải absolute risk
- D. Absolute risk và relative risk là **như nhau**
- E. Nguy cơ tuyệt đối trọn đời phụ thuộc cả tuổi/thời gian quan sát

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B, C, E** — đúng.
- ❌ **D** — sai: hai khái niệm **khác nhau**.
</details>

---

### Câu 6 · 🔴 Rất khó
Về **hai bài toán ML ung thư** & dữ liệu:
- A. **Cancer Subtyping** → phục vụ **chẩn đoán / patient stratification**
- B. **Drug Response Prediction** → phục vụ **điều trị**
- C. Cả hai dùng đặc trưng: CNV, mutation, methylation, gene expression, clinical data
- D. **NCI-DREAM** gồm sub-challenge **Drug Sensitivity** và **Drug Synergy**
- E. **CCLE / GDSC / CTRP** là CSDL cell line multi-omics (>1000 cell line)
- F. Cancer subtyping và drug response dùng **hai bộ đặc trưng hoàn toàn khác nhau**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A, B, C, D, E** — đúng.
- ❌ **F** — sai: cả hai dùng **cùng bộ đặc trưng** genomic, chỉ khác **mục tiêu**.
</details>

---

### Câu 7 · 🟠 Khó
Về **cell line** & cách tiếp cận tích hợp:
- A. Cell line = nuôi cấy từ **1 tế bào** → đồng nhất di truyền
- B. Chuỗi: **Patient → Tumor → Cell line**
- C. Cách tiếp cận: **network-based** & **machine learning-based** (ngày càng dùng DL + GNN)
- D. Cell line **không** dùng được cho nghiên cứu drug response
- E. CTRP gồm bộ **481 hợp chất** phân tử nhỏ

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B, C, E** — đúng.
- ❌ **D** — sai: cell line **là nền tảng** cho nghiên cứu drug response.
</details>

---

### Câu 8 · 🟢 TB
Về sinh dữ liệu -omics & tài nguyên:
- A. Omics là **big data** → cần AI
- B. Thách thức: **translational research** ("from bench to bedside")
- C. **DMET chip**: 1936 SNP trên 231 gene (dùng PGx)
- D. **gnomAD** (tiền thân ExAC), **COSMIC** (đột biến soma), **TCGA/GDC**
- E. Omics data luôn nhỏ, xử lý được bằng tay

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: omics là **big data**, không xử lý bằng tay.
</details>

---

### Câu 9 · 🔴 Rất khó
Chọn **TẤT CẢ** phát biểu **SAI**:
- A. Pharmacogenomics tích hợp toàn bộ đa -omics của cá nhân
- B. Trục Y của Manhattan plot là P-value (không lấy log)
- C. PRS cho nguy cơ tuyệt đối chính xác cho mọi chủng tộc
- D. Cancer subtyping phục vụ điều trị; drug response phục vụ chẩn đoán
- E. Proteomics là toàn bộ RNA của tế bào

<details><summary>▸ Đáp án</summary>

**SAI: A, B, C, D, E** (cả 5 đều sai)

- ❌ **A** — đó là **Personalized Medicine**, không phải PGx (PGx = chỉ genomics).
- ❌ **B** — trục Y là **−log(P)**.
- ❌ **C** — PRS = relative risk, thiên lệch gốc Âu, là xác suất.
- ❌ **D** — đảo ngược: subtyping → chẩn đoán, drug response → điều trị.
- ❌ **E** — proteomics = **protein** (RNA là transcriptomics).
</details>

---

### Câu 10 · 🟢 TB
Các loại **xét nghiệm gen (genetic testing)**:
- A. **Predictive** (có người thân mắc bệnh di truyền)
- B. **Diagnostic** (chẩn đoán xác nhận)
- C. **Pharmacogenomic** (phản ứng thuốc)
- D. **Reproductive** (sinh sản)
- E. **Forensic** (pháp y) & **Direct-to-consumer** (tại nhà)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E** (tất cả đều là loại genetic testing hợp lệ)

- ✅ Cả 5 đúng — câu "an toàn" để chắc điểm; cảnh giác vì multiple-select đôi khi tất cả đều đúng.
</details>
