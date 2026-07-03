# Chương 1 – Giới thiệu về AI tạo sinh trong Tin sinh học, Y học và Chăm sóc sức khỏe

> Môn: **IT5428 – Generative AI in Bioinformatics, Medicine and Healthcare**
> Chương này đặt bối cảnh: *tại sao* cần AI (đặc biệt AI tạo sinh) trong y sinh, và *những bài toán ứng dụng* xuyên suốt môn học.

> **🔖 Quy ước nhãn xác suất ra thi (dùng cho cả 6 chương):**
> - 🔴 **CAO** – gần như chắc chắn có câu hỏi; học kỹ, thuộc số liệu & định nghĩa.
> - 🟡 **TB** – có khả năng ra; nắm ý chính + ví dụ.
> - ⚪ **THẤP** – đọc để hiểu mạch, ít khi hỏi trực tiếp.
>
> *(Đánh giá dựa trên: mức nhấn mạnh trong slide, khái niệm có định nghĩa/so sánh rõ, số liệu "đắt", và mức độ lặp lại xuyên suốt môn.)*

---

## 1.0. Thông tin môn học ⚪ THẤP
- **Đánh giá**: Mid-term **50%** + Final-term **50%**.
- Nội dung chia 2 hướng:
  - **Research-oriented** → *Computational Biomedicine (CBM)*.
  - **Application-oriented** → *Genome Analysis Pipelines* (chính là pipeline GATK ở Ch4).
- Hai chủ đề tổng: **Genetic Background of Diseases** (nền tảng di truyền của bệnh) & **Drug Discovery** (khám phá thuốc).

---

## 1.1. Các khái niệm nền tảng cần nắm 🔴 CAO

| Khái niệm | Ý nghĩa |
|---|---|
| **Bioinformatics (Tin sinh học)** | Dùng phương pháp tính toán (AI, toán, thống kê) để xây dựng và phân tích dữ liệu y sinh **thông lượng cao (high-throughput)**. |
| **Computational Biomedicine (CBM)** | Tích hợp dữ liệu **đa tầng (multi-level)** → xây CSDL lớn → khám phá tri thức mới → hỗ trợ nghiên cứu & ứng dụng lâm sàng (**sàng lọc – chẩn đoán – điều trị**). |
| **AI phân biệt (Discriminative)** | Học **ranh giới quyết định** `P(Y\|X)` cho phân loại/hồi quy (thường học **có giám sát**). |
| **AI tạo sinh (Generative)** | Học **phân phối dữ liệu** `P(X)` (thường **không giám sát**); có thể **lấy mẫu để sinh dữ liệu mới**, hoặc học có điều kiện `P(X\|Y)`. |

> 🎯 **Bẫy hay gặp:** đảo ngược discriminative ↔ generative. Nhớ chốt: *discriminative học `P(Y|X)` (ranh giới); generative học `P(X)` (phân phối, sinh được dữ liệu)*.

**Vì sao AI tạo sinh quan trọng trong y sinh?** 🟡 TB
- Dữ liệu y sinh là **big data**, nhưng **thưa nhãn** (labels sparse, biased, chất lượng thay đổi).
- Sinh dữ liệu nhân tạo (artificial genomes, phân tử thuốc mới) giúp: bảo vệ **quyền riêng tư (privacy)**, **tăng cường dữ liệu (data augmentation)**, **đại diện quần thể thiếu dữ liệu**.
- Có thể **suy diễn khi thiếu nhãn** (ví dụ dự đoán biến thể gây bệnh mà không cần nhãn ClinVar → xem EVE ở Ch4).

---

## 1.2. Các ứng dụng động lực (motivating applications)

### a) Nền tảng di truyền của bệnh (Genetic Background of Diseases) 🟡 TB
- **Bệnh di truyền tăng theo tuổi:** ~**5% ở trẻ sơ sinh** → ~**5% người lớn < 25 tuổi** → ~**60% người cao tuổi**. (Số liệu dễ hỏi.)
- Không chỉ **gen mã hóa protein** (protein-coding) mà cả vùng **non-coding**.
- Không chỉ bệnh **đơn gen (monogenic)** mà còn bệnh **đa gen (polygenic)** → nền cho GWAS/PRS (Ch5).

### b) Sàng lọc sơ sinh & trước sinh bằng xét nghiệm gen 🟡 TB
- **Thalassemia (tan máu bẩm sinh)**: hemoglobin cấu trúc bất thường → hồng cầu bị phá hủy → thiếu máu nghiêm trọng.
  - *Beta-thalassemia*: không tạo đủ **beta-globin** → sức ép lên gan, lách, tủy xương; biến chứng suy tim, xơ gan, lách to.
  - Đột biến ở **gene beta-globin** — cùng gen liên quan **sickle cell disease** (hồng cầu hình liềm).
- **Duchenne muscular dystrophy (teo cơ Duchenne)**: bệnh di truyền liên kết X.
- **NIPT (Non-Invasive Prenatal Testing)** – sàng lọc trước sinh **không xâm lấn**, dựa vào **cfDNA (cell-free fetal DNA)** của thai trong máu mẹ → giải trình tự → phát hiện bất thường số lượng NST.
  - Phát hiện: **Down (Trisomy 21)**, **Edwards (Trisomy 18)**, **Patau (Trisomy 13)**; ở NST giới tính: **Turner (XO)**, **XYY ("super man")**.

### c) Phát hiện & điều trị ung thư 🔴 CAO
> Ung thư là **ca ứng dụng trung tâm** của cả môn — quay lại ở Ch2, Ch4 (Mutect2), Ch5, Ch6.

- **Oncogene (gen sinh ung thư)** – *gain-of-function*: **KRAS, EGFR, BRAF**.
  - *KRAS*: đột biến khiến protein **luôn hoạt hóa** → tế bào liên tục nhận tín hiệu sinh sản → tăng sinh không kiểm soát.
- **Tumor suppressor (gen ức chế khối u)** – *loss-of-function*: **TP53 (p53)**, RB1, PTEN.
  - *p53*: làm chậm phân chia, sửa DNA lỗi, khởi động **apoptosis** (chết theo chương trình). Mất chức năng → ung thư.
- **Điều trị đích (targeted therapy)**: phát hiện đột biến của bệnh nhân → chọn thuốc tác động đúng gen/protein đặc hiệu của tế bào ung thư.
- **BRCA1/BRCA2**: hai gen đầu tiên liên quan ung thư vú/buồng trứng di truyền; là **tumor suppressor** (cần mất chức năng cả 2 copy).

> 🎯 **Bẫy:** đảo ngược *oncogene (gain-of-function)* ↔ *tumor suppressor (loss-of-function)*, hoặc gán nhầm ví dụ (TP53 là suppressor, không phải oncogene).

### d) Vi khuẩn kháng thuốc (antibiotic resistance) 🟡 TB
- Ví dụ *Klebsiella pneumoniae*, *Acinetobacter baumannii* – đa kháng (mang gen kháng thuốc).
- **2 bài toán ML cần giải:**
  1. Chủng nguy hiểm mới → **dự đoán kháng sinh nào còn nhạy**.
  2. Đề xuất **cơ chế kháng thuốc mới** & **thuốc điều trị mới**.

### e) Chi phí giải trình tự DNA giảm nhanh ⚪ THẤP
- Human Genome Project (~$3 tỷ) → nay giảm mạnh (genome.gov "DNA Sequencing Costs"). Đây là **động lực bùng nổ dữ liệu genomics**.

---

## 1.3. ⭐ Bài toán Disease–Gene–Drug (khung xuyên suốt môn) 🔴 CAO

> Đây là "khung tư duy" của cả CBM. Rất hay ra ở dạng: *"Dự đoán mối liên kết nào?"*, *"Cách tiếp cận nào?"*.

**3 loại liên kết cần dự đoán:**
| Liên kết | Nghĩa |
|---|---|
| **Drug–Target Interaction (DTI)** | Thuốc gắn vào đích (protein/gene) nào? |
| **Disease–Gene Association (DGA)** | Gen nào liên quan bệnh nào? |
| **Drug–Disease Association** | Thuốc trị bệnh nào → **drug repositioning/repurposing** |

**Dữ liệu biểu diễn đối tượng (annotation data):** Structure (cấu trúc), String/Sequence (chuỗi), **Network (mạng)**, Text (ontology, y văn)…

**3 cách tiếp cận tính toán:** 🔴 CAO
- **Network-based** – dựa **nguyên lý module bệnh (disease module principle)**: *gen/protein liên quan cùng/tương tự một kiểu hình bệnh thì nằm gần nhau trong mạng sinh học* → dùng **network ranking / label propagation** (vd Heter-LP).
- **Machine Learning-based** – biểu diễn gen/protein bằng **feature vector** → phân loại. Do thiếu nhãn âm (negative), hay dùng: **unary classification**, **PU learning (Positive-Unlabeled)**, **binary semi-supervised classification**.
- **Data mining-based**.

### Drug-Target Interaction – 3 dạng (nhớ ví dụ điển hình) 🔴 CAO
| Dạng | Ví dụ điển hình |
|---|---|
| **1 thuốc – 1 đích** | **Albuterol** (giảm hen suyễn) tác động thụ thể **beta2AR** trên màng tế bào phổi; beta2AR mã hóa bởi gen **ADRB2** |
| **Nhiều thuốc – 1 đích** | **ZMapp** trị Ebola = **hỗn hợp 3 kháng thể đơn dòng (monoclonal antibodies)** cùng gắn protein virus Ebola (EVD tỷ lệ tử vong ~50%) |
| **1 thuốc – nhiều đích** | **Imatinib** – đa đích, trị **bạch cầu tủy mạn (CML)** và **bạch cầu lympho cấp (ALL)** |

### Drug Repositioning (tái định vị thuốc) 🟡 TB
- **Định nghĩa**: lấy thuốc phát triển cho bệnh này → dùng cho bệnh khác (*repositioning / repurposing*).
- **3 mô hình phát triển thuốc:**
  1. **Known target → compound screening** (biết đích, sàng lọc hợp chất mới).
  2. **Known compound → target screening** (biết hợp chất, tìm đích mới).
  3. **Withdrawn/marketed drug → repositioning** (thuốc đã có → chỉ định mới).
- **Số liệu "đắt":** ước tính ~**75%** thuốc *về lý thuyết* có thể tái định vị (Bernard Munos); thuốc tái định vị có thể chiếm ~**30%** thuốc được duyệt mỗi năm; mỗi thuốc lâu năm có ~**20 công dụng off-label**.
- Ví dụ: **ebselen** (vốn cho đột quỵ) → ức chế inositol monophosphatase giống lithium → tiềm năng trị **rối loạn lưỡng cực (bipolar)**.

---

## 1.4. Bản đồ toàn môn học (6 chương)

| Chương | Chủ đề | File ôn tập |
|---|---|---|
| **1** | Giới thiệu GenAI trong tin sinh/y học | *(file này)* |
| **2** | Cơ chế sinh học phân tử của tế bào | [Chuong2_SinhHocPhanTu.md](Chuong2_SinhHocPhanTu.md) |
| **3** | Khám phá thuốc (Drug Discovery) | [Chuong3_KhamPhaThuoc.md](Chuong3_KhamPhaThuoc.md) |
| **4** | Phân tích hệ gen (Genome Analysis + GATK) ⭐ | [Chuong4_PhanTichHeGen.md](Chuong4_PhanTichHeGen.md) |
| **5** | Y học cá thể hóa (Personalized Medicine) | [Chuong5_YHocCaTheHoa.md](Chuong5_YHocCaTheHoa.md) |
| **6** | Trí tuệ nhân tạo diễn giải (Explainable AI) | [Chuong6_AI_DienGiai_XAI.md](Chuong6_AI_DienGiai_XAI.md) |

---

## 1.5. 🎯 Điểm tủ Chương 1 (dễ ra thi nhất)
1. 🔴 **Discriminative `P(Y|X)` vs Generative `P(X)`** – định nghĩa, ví dụ, đâu là học không giám sát.
2. 🔴 **Disease–Gene–Drug** – 3 loại liên kết + 3 cách tiếp cận (network/ML/data mining) + disease module principle.
3. 🔴 **Oncogene vs Tumor suppressor** – gain vs loss of function, ví dụ (KRAS/EGFR/BRAF vs TP53/RB1/PTEN/BRCA).
4. 🟡 **Drug-Target Interaction 3 dạng** + ví dụ (Albuterol/ADRB2, ZMapp/Ebola, Imatinib).
5. 🟡 **NIPT** – nguyên lý cfDNA, phát hiện Trisomy 21/18/13.
6. 🟡 **Lý do cần GenAI** – 3 lợi ích sinh dữ liệu nhân tạo (privacy, augmentation, đại diện quần thể).
7. ⚪ Số liệu: 5%/5%/60% bệnh di truyền theo tuổi; 75% & 30% drug repositioning; HGP $3 tỷ.

## 1.6. Câu hỏi ôn tập nhanh
1. Phân biệt mô hình **discriminative** và **generative**? Cho ví dụ trong genomics.
2. NIPT hoạt động dựa trên nguyên lý sinh học nào? Phát hiện được các hội chứng nào?
3. Phân biệt **oncogene** và **tumor suppressor gene**; cho ví dụ và cơ chế (KRAS vs TP53).
4. Vẽ khung **Disease–Gene–Drug**: 3 liên kết cần dự đoán, 3 cách tiếp cận, nguyên lý module bệnh.
5. Kể 3 dạng **Drug-Target Interaction** kèm ví dụ; drug repositioning là gì, vì sao hấp dẫn?
6. Vì sao dữ liệu genomics cần AI tạo sinh? Nêu 3 lợi ích của **sinh dữ liệu gen nhân tạo**.
