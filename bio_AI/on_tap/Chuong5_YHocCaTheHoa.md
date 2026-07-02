# Chương 5 – Y học cá thể hóa (Personalized / Precision Medicine)

> Mục tiêu của y học hiện đại: đúng bệnh nhân – đúng thuốc – đúng liều – đúng thời điểm, dựa trên dữ liệu **-omics** cá nhân.

---

## 5.1. Khái niệm cốt lõi ⭐
- **Precision / Stratified Medicine**: chia bệnh nhân thành nhóm → điều trị phù hợp (đúng liều, đúng thời điểm).
- **Pharmacogenomics (PGx)**: tối ưu liệu pháp dựa trên **nội dung genomics** của bệnh nhân (dự đoán đáp ứng & phản ứng có hại của thuốc – ADR).
- **Personalized Medicine**: không chỉ genomics mà tích hợp **đa -omics** của cá nhân (transcriptomics, proteomics, interactomics...).

## 5.2. ⭐ Kỷ nguyên dữ liệu -omics
Theo **Central Dogma**: DNA → RNA → Protein → Metabolite.

| -omics | Đối tượng | Định nghĩa |
|---|---|---|
| **Genomics** | DNA/gen | Toàn bộ chỉ dẫn di truyền ("bản thiết kế") |
| **Transcriptomics** | RNA | Toàn bộ RNA – "ảnh chụp" biểu hiện gen tại 1 thời điểm (RNA-seq, microarray) |
| **Proteomics** | Protein | Toàn bộ protein – "đầu ra chức năng" của genome |
| **Metabolomics** | Metabolite | Toàn bộ phân tử nhỏ (amino acid, đường, lipid, nucleotide, vitamin) |
| **Interactomics** | Tương tác | Mạng tương tác phân tử |

- Omics là **big data** → cần phương pháp tính toán (AI). Thách thức lớn: **translational research** – "from bench to bedside" (từ phòng thí nghiệm ra giường bệnh).

## 5.3. Sinh dữ liệu -omics (genomic data)
- **WGS** (3,1 tỷ bp), **WES** (~1,4% WGS), **DMET chip** (1936 SNP trên 231 gene – PGx), genotyping.
- Quy trình: Blood → DNA → Sequencing → **Analysis pipeline (GATK)** → variants.
- CSDL: **TCGA, GDC portal, COSMIC** (đột biến soma ung thư), **gnomAD** (ExAC).

## 5.4. ⭐ Các bài toán tính toán trong Y học cá thể hóa

### Bài toán #1 – Sàng lọc / Screening (nguy cơ bệnh)
- Nguy cơ mắc bệnh của cá nhân so với quần thể?
- Công cụ: **Polygenic Risk Score (PRS)**.

### Bài toán #2 – Điều trị cá thể hóa (Drug Response)
- Bệnh nhân đáp ứng thuốc thế nào dựa trên hồ sơ genomics?

**Dữ liệu nghiên cứu (cell line):** **CCLE, GDSC, CTRP** – >1000 cell line, dữ liệu multi-omics (genomics + transcriptomics + drug response). Cell line = nuôi cấy từ 1 tế bào, đồng nhất di truyền. Patient → Tumor → Cell line.

**Hai bài toán ML chính:**
1. **Cancer Subtyping** (phân nhóm ung thư): stratify bệnh nhân/khối u thành subtype dựa trên **CNV, mutation, methylation, gene expression, clinical data**.
2. **Drug Response Prediction**: dự đoán nhóm đáp ứng tốt / phản ứng phụ / không đáp ứng.
   - Vd: Responder vs Non-responder (nhị phân), hoặc Responder/Intermediate/Non-responder.
   - Thử thách chuẩn: **NCI-DREAM** (Drug Sensitivity Challenge, Drug Synergy Challenge).

**Cách tiếp cận tích hợp (integration methods):**
- **Network-based** (dựa trên mạng sinh học – disease module principle).
- **Machine learning-based** (biểu diễn feature vector cho gene/protein).
- Ngày càng dùng **Deep Learning + GNN + multi-omics integration**.

## 5.5. ⭐ GWAS (Genome-Wide Association Study)
- So sánh genome của người **có bệnh (case)** và **không bệnh (control)** → tìm biến thể xuất hiện thường xuyên hơn ở nhóm bệnh.
- Dữ liệu: bảng Sample × Variant → Outcome (disease status / drug response).
- Kết quả trực quan hóa bằng **Manhattan plot**: trục Y = **-log(P-value)** (càng cao càng có ý nghĩa).
- Có thể có hàng trăm–hàng nghìn biến thể/bệnh; **không cần biết gene cụ thể** để ước lượng nguy cơ.

## 5.6. ⭐ Polygenic Risk Score (PRS)
- Dùng **chỉ thông tin genomics** để đánh giá nguy cơ mắc bệnh, dựa trên **sự có mặt/vắng mặt của nhiều biến thể** (không tính yếu tố môi trường).
- **Quy trình:**
  1. GWAS xác định biến thể liên quan bệnh (so case vs control).
  2. Dùng thống kê tính điểm tổng hợp từ tập biến thể của 1 người → PRS.
- **Đặc điểm & giới hạn quan trọng** (hay hỏi):
  - PRS chỉ giải thích **nguy cơ tương đối (relative risk)**, không phải **tuyệt đối (absolute risk)**. (Vd BRCA1 → nguy cơ tuyệt đối 60-80% ung thư vú).
  - **Chỉ tương quan, không nhân quả (correlation ≠ causation)**.
  - Không cho biết mốc/thời gian tiến triển bệnh (2 người cùng PRS nhưng 22 tuổi vs 98 tuổi → nguy cơ trọn đời khác nhau).
  - Phân phối theo **đường cong chuông**: đa số ở giữa (nguy cơ trung bình); đuôi = thấp/cao.
  - **Vấn đề đa dạng chủng tộc**: phần lớn dữ liệu từ **người gốc Âu** → PRS có thể **chỉ chính xác cho quần thể gốc Âu** → lo ngại bất bình đẳng y tế. (Động lực cho dự án DGV4VN cho người Việt).
  - Chưa dùng thường quy lâm sàng (thiếu guideline); luôn là **xác suất, không phải chắc chắn**.

## 5.7. Ứng dụng trong xét nghiệm gen (genetic testing)
- **Predictive** (dự đoán – có người thân mắc bệnh di truyền), **Diagnostic** (chẩn đoán xác nhận), **Pharmacogenomic** (phản ứng thuốc), **Reproductive** (sinh sản), **Direct-to-consumer** (tại nhà), **Forensic** (pháp y).

---

## 5.8. Câu hỏi ôn tập nhanh
1. Phân biệt **Precision Medicine, Pharmacogenomics, Personalized Medicine**.
2. Kể **4 loại -omics** và đối tượng mỗi loại. Liên hệ với Central Dogma.
3. **GWAS** hoạt động thế nào? Manhattan plot biểu diễn gì?
4. **PRS** là gì, tính thế nào? Vì sao chỉ là **nguy cơ tương đối** và có **vấn đề đa dạng chủng tộc**?
5. Hai bài toán ML chính trong y học cá thể hóa ung thư? Cách tiếp cận tích hợp?
6. Phân biệt **absolute risk vs relative risk**; correlation vs causation trong PRS.
