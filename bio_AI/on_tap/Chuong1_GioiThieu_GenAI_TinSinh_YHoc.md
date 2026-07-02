# Chương 1 – Giới thiệu về AI tạo sinh trong Tin sinh học, Y học và Chăm sóc sức khỏe

> Môn: **IT5428 – Generative AI in Bioinformatics, Medicine and Healthcare**
> Chương này đặt bối cảnh: *tại sao* cần AI (đặc biệt AI tạo sinh) trong y sinh, và *những bài toán ứng dụng* xuyên suốt môn học.

---

## 1.1. Các khái niệm nền tảng cần nắm

| Khái niệm | Ý nghĩa |
|---|---|
| **Bioinformatics (Tin sinh học)** | Dùng phương pháp tính toán (AI, toán, thống kê) để xây dựng và phân tích dữ liệu y sinh thông lượng cao (high-throughput). |
| **Computational Biomedicine (CBM)** | Tích hợp dữ liệu đa tầng → xây CSDL lớn → khám phá tri thức mới → hỗ trợ nghiên cứu & ứng dụng lâm sàng (sàng lọc, chẩn đoán, điều trị). |
| **AI phân biệt (Discriminative)** | Mô hình học ranh giới quyết định `P(Y|X)` cho phân loại/hồi quy (học có giám sát). |
| **AI tạo sinh (Generative)** | Mô hình học **phân phối dữ liệu** `P(X)` (thường không giám sát); có thể lấy mẫu để sinh dữ liệu mới, hoặc học có điều kiện `P(X|Y)`. |

**Vì sao AI tạo sinh quan trọng trong y sinh?**
- Dữ liệu y sinh là **big data**, thưa nhãn (labels sparse, biased, chất lượng thay đổi).
- Sinh dữ liệu nhân tạo (artificial genomes, phân tử thuốc mới) giúp: bảo vệ **quyền riêng tư**, **tăng cường dữ liệu** (data augmentation), đại diện quần thể thiếu dữ liệu.
- Có thể suy diễn khi thiếu nhãn (ví dụ dự đoán biến thể gây bệnh mà không cần nhãn ClinVar).

---

## 1.2. Các ứng dụng động lực (motivating applications)

### a) Sàng lọc sơ sinh & trước sinh bằng xét nghiệm gen
- **Bệnh tan máu bẩm sinh Thalassemia**: hemoglobin có cấu trúc bất thường → hồng cầu bị phá hủy → thiếu máu nghiêm trọng.
  - *Beta-thalassemia*: cơ thể không tạo đủ **beta-globin** → sức ép lên gan, lách, tủy xương; biến chứng: suy tim, xơ gan, lách to.
  - Đột biến ở **gene beta-globin** (liên hệ với *sickle cell disease* – hồng cầu hình liềm).
- **Xét nghiệm NIPT (Non-Invasive Prenatal Testing)**: sàng lọc trước sinh **không xâm lấn**, dựa vào **DNA tự do của thai nhi (cfDNA)** trong máu mẹ → giải trình tự → phát hiện bất thường số lượng/đột biến nhiễm sắc thể.
  - Phát hiện: **Hội chứng Down (Trisomy 21)**, **Edwards (Trisomy 18)**, **Patau (Trisomy 13)**.

### b) Phát hiện & điều trị ung thư
- **Gen gây ung thư (oncogene)**: ví dụ **KRAS, EGFR, BRAF**.
  - *KRAS*: mã hóa protein KRAS. Đột biến "tăng chức năng" (gain-of-function) làm KRAS **luôn hoạt hóa** → tế bào liên tục nhận tín hiệu sinh sản → tăng sinh không kiểm soát.
- **Gen ức chế khối u (tumor suppressor)**: ví dụ **TP53 (p53)**, RB1, PTEN.
  - *p53*: làm chậm phân chia tế bào, sửa DNA lỗi, khởi động **apoptosis** (chết theo chương trình). Khi mất chức năng → tăng sinh không kiểm soát → ung thư.
- **Điều trị đích (targeted therapy)**: dùng thuốc tác động vào gen/protein đặc hiệu của tế bào ung thư → phát hiện đột biến bệnh nhân → đề xuất thuốc điều trị đích.
- **BRCA1/BRCA2**: hai gen đầu tiên liên quan ung thư vú/buồng trứng di truyền; là tumor suppressor. (Ví dụ Angelina Jolie mang BRCA1 lỗi → nguy cơ cao).

### c) Vi khuẩn kháng thuốc (antibiotic resistance)
- Ví dụ *Klebsiella pneumoniae*, *Acinetobacter baumannii* – đa kháng kháng sinh (mang gen kháng thuốc).
- **Bài toán ML cần giải**:
  1. Khi phát hiện chủng nguy hiểm mới → **dự đoán kháng sinh nào còn nhạy** với chủng đó.
  2. Đề xuất **cơ chế kháng thuốc mới** & **thuốc điều trị mới**.

### d) Chi phí giải trình tự DNA giảm nhanh
- Human Genome Project (~$3 tỷ) → nay chi phí giảm mạnh (tham chiếu genome.gov "DNA Sequencing Costs"). Đây là động lực làm bùng nổ dữ liệu genomics.

---

## 1.3. Bản đồ toàn môn học (6 chương)

| Chương | Chủ đề | File ôn tập |
|---|---|---|
| **1** | Giới thiệu GenAI trong tin sinh/y học | *(file này)* |
| **2** | Cơ chế sinh học phân tử của tế bào | `Chuong2_SinhHocPhanTu.md` |
| **3** | Khám phá thuốc (Drug Discovery) | `Chuong3_KhamPhaThuoc.md` |
| **4** | Phân tích hệ gen (Genome Analysis + GATK) | `Chuong4_PhanTichHeGen.md` |
| **5** | Y học cá thể hóa (Personalized Medicine) | `Chuong5_YHocCaTheHoa.md` |
| **6** | Trí tuệ nhân tạo diễn giải (Explainable AI) | `Chuong6_AI_DienGiai_XAI.md` |

**Bài toán Disease–Gene–Drug** (chủ đề xuyên suốt chương 4 & 5): dự đoán các liên kết
- **Drug–Target Interaction** (tương tác thuốc–đích),
- **Disease–Gene Association** (liên kết bệnh–gen),
- **Drug–Disease Association** (tái định vị thuốc / drug repositioning).

Các cách tiếp cận tính toán: **network-based**, **machine learning-based**, **data mining-based**.

---

## 1.4. Câu hỏi ôn tập nhanh
1. Phân biệt mô hình **discriminative** và **generative**? Cho ví dụ trong genomics.
2. NIPT hoạt động dựa trên nguyên lý sinh học nào? Phát hiện được các hội chứng nào?
3. Phân biệt **oncogene** và **tumor suppressor gene**; cho ví dụ và cơ chế (KRAS vs TP53).
4. Vì sao dữ liệu genomics cần các phương pháp AI? Nêu 3 lợi ích của việc **sinh dữ liệu gen nhân tạo**.
5. Hai bài toán ML nào cần giải với vi khuẩn kháng thuốc?
