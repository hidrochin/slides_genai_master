# 📚 Tổng quan ôn tập – IT5428: AI Tạo Sinh trong Tin sinh học, Y học & Chăm sóc sức khỏe

> Bộ tài liệu ôn tập tổng hợp từ toàn bộ slide bài giảng. Đọc theo thứ tự 6 chương; file này cho **cái nhìn xuyên suốt + mẹo thi**.

## 🗂️ Danh sách file
| Chương | File | Trọng tâm |
|---|---|---|
| 1 | [Chuong1_GioiThieu_GenAI_TinSinh_YHoc.md](Chuong1_GioiThieu_GenAI_TinSinh_YHoc.md) | Bối cảnh, ứng dụng động lực, discriminative vs generative |
| 2 | [Chuong2_SinhHocPhanTu.md](Chuong2_SinhHocPhanTu.md) | Central Dogma, protein, DNA/RNA, phiên mã/dịch mã |
| 3 | [Chuong3_KhamPhaThuoc.md](Chuong3_KhamPhaThuoc.md) | PK/PD/ADME, quy trình khám phá thuốc, SMILES, GNN, VAE/GAN |
| 4 | [Chuong4_PhanTichHeGen.md](Chuong4_PhanTichHeGen.md) | ⭐ GATK pipeline, germline/somatic, GenAI genomics, EVE/AlphaFold |
| 5 | [Chuong5_YHocCaTheHoa.md](Chuong5_YHocCaTheHoa.md) | -omics, GWAS, PRS, drug response, cancer subtyping |
| 6 | [Chuong6_AI_DienGiai_XAI.md](Chuong6_AI_DienGiai_XAI.md) | XAI, SHAP/LIME/Grad-CAM, 5 chiều đánh giá |

*(Text đầy đủ trích từ PDF nằm trong thư mục `../extracted/`.)*

---

## 🔖 Hệ thống nhãn "xác suất ra thi" (mới thêm)

Mỗi mục trong 6 file chương giờ được gắn nhãn mức độ có thể xuất hiện trong đề trắc nghiệm:

| Nhãn | Ý nghĩa | Cách học |
|---|---|---|
| 🔴 **CAO** | Gần như chắc chắn có câu hỏi | Học kỹ, thuộc **định nghĩa + số liệu + so sánh** |
| 🟡 **TB** | Có khả năng ra | Nắm **ý chính + 1 ví dụ** |
| ⚪ **THẤP** | Ít khi hỏi trực tiếp | Đọc để hiểu mạch, không cần thuộc |

- Mỗi chương có thêm mục **"🎯 Điểm tủ"** ở gần cuối: liệt kê các câu tủ theo thứ tự ưu tiên (học từ trên xuống nếu ít thời gian).
- Rải rác trong bài có các hộp **"🎯 Bẫy"**: chỉ ra kiểu phương án sai thường gặp (đảo ngược cặp khái niệm, gán nhầm ví dụ, dùng từ tuyệt đối).
- Cơ sở đánh giá nhãn: mức nhấn mạnh trong slide (⭐), khái niệm có định nghĩa/so sánh rõ, số liệu "đắt", và mức lặp lại xuyên suốt môn.

> **Chiến lược ôn nước rút:** quét toàn bộ mục 🔴 của cả 6 chương trước → sau đó làm bộ `../trac_nghiem/` → sai đâu quay lại đọc mục tương ứng.

---

## 🔗 Sợi chỉ đỏ xuyên suốt môn học

**1. Central Dogma là nền tảng của mọi thứ:**
```
DNA → RNA → Protein → (Metabolite)
 │      │       │
Genomics  Transcriptomics  Proteomics   ← các tầng -omics (Ch5)
 │
Biến thể (SNV/indel/SV) → GATK phát hiện (Ch4) → diễn giải bệnh (Ch4,5)
```

**2. AI tạo sinh (Generative AI) – bộ công cụ lặp lại ở nhiều chương:**
| Mô hình | Xuất hiện ở | Ý chính |
|---|---|---|
| **VAE** | Ch3 (sinh phân tử), Ch4 (PopVAE, EVE, artificial genomes) | Encoder→phân phối latent→decoder; sinh dữ liệu bằng lấy mẫu |
| **GAN / WGAN** | Ch3 (sinh phân tử), Ch4 (phyloGAN, artificial genomes) | Generator vs Discriminator/Critic đối kháng |
| **GNN** | Ch3 (molecular graph), Ch4-5 (mạng sinh học) | Message passing trên đồ thị |
| **RBM / CRBM** | Ch4 (artificial genomes) | Học phân phối, 2 lớp visible-hidden |
| **Transformer / Foundation model** | Ch4 (AlphaMissense, EVO, AlphaFold) | Nền tảng lớn, đa mô thức |

**3. Bài toán Disease–Gene–Drug** (Ch4, Ch5): Drug-Target Interaction, Disease-Gene Association, Drug-Disease (repositioning) – giải bằng network-based / ML-based.

**4. Ung thư là ca ứng dụng trung tâm:** oncogene/tumor suppressor (Ch1,2) → somatic variant + CNV calling GATK/Mutect2 (Ch4) → cancer subtyping & drug response (Ch5) → diễn giải bằng SHAP/Grad-CAM (Ch6).

---

## 🎯 Bảng thuật ngữ "phải thuộc" (glossary tốc độ)

| Thuật ngữ | Nghĩa nhanh |
|---|---|
| **Germline vs Somatic** | Di truyền được (mọi tế bào) vs chỉ ở khối u (không di truyền) |
| **SNV/SNP, Indel, CNV, SV** | Biến thể 1 nucleotide / thêm-mất nhỏ / số bản sao / cấu trúc lớn |
| **FASTQ→BAM→VCF** | Read thô → đã align → biến thể |
| **BWA** | Công cụ map read vào reference |
| **BQSR** | Hiệu chỉnh base quality bằng ML (cần dbSNP) |
| **HaplotypeCaller** | Gọi germline variant (4 giai đoạn, De Bruijn graph, PairHMM, Bayes) |
| **GVCF / GenomicsDBImport / GenotypeGVCFs** | Workflow cohort, giải quyết N+1 problem |
| **VQSR / VQSLOD** | Lọc biến thể bằng ML trên cohort |
| **CNNScoreVariants** | Lọc biến thể bằng deep learning (single-sample) |
| **Mutect2** | Gọi somatic variant (Tumor-Normal) |
| **PoN (Panel of Normals)** | Loại artifact kỹ thuật & germline phổ biến |
| **Strand bias vs Orientation bias** | Lệch theo sợi DNA vs lệch theo hướng map (F1R2/F2R1) |
| **Funcotator / VEP** | Annotate chức năng biến thể |
| **Nonsense/Missense/Frameshift** | Stop sớm / đổi aa / lệch khung đọc |
| **EVE / AlphaMissense** | Dự đoán biến thể gây bệnh (Bayesian VAE / fine-tune AlphaFold) |
| **PK/PD/ADME** | Cơ thể↔thuốc / Hấp thu-Phân bố-Chuyển hóa-Thải trừ |
| **SMILES/SELFIES/InChI** | Biểu diễn phân tử thuốc dạng chuỗi |
| **QSAR / Morgan fingerprint** | Cấu trúc↔hoạt tính / vân tay phân tử |
| **-omics** | Genomics/Transcriptomics/Proteomics/Metabolomics |
| **GWAS / Manhattan plot** | So case-control tìm biến thể / plot -log(P) |
| **PRS** | Điểm nguy cơ đa gen (nguy cơ **tương đối**) |
| **LD / Haplotype / MAF** | Liên kết không cân bằng / nhóm biến thể / tần số allele phụ |
| **SHAP / LIME / Grad-CAM** | Phương pháp diễn giải post-hoc |
| **Intrinsic vs Post-hoc** | Mô hình tự diễn giải vs giải thích sau |
| **Hallucination / RAG** | Ảo giác của GenAI / truy xuất tăng cường để kiểm chứng |

---

## 📝 Chủ đề dễ ra thi (dự đoán trọng tâm)

1. **Central Dogma** + phiên mã/dịch mã/splicing (Ch2) – câu nền tảng gần như chắc chắn.
2. **Pipeline GATK** – vẽ sơ đồ tiền xử lý → germline (GVCF workflow) → somatic (Mutect2) – **trọng tâm nhất của môn**.
3. **HaplotypeCaller 4 giai đoạn** & **N+1 problem**.
4. **Germline vs Somatic**, **strand bias vs orientation bias**.
5. **VAE vs GAN vs AE** – so sánh, mode collapse, ứng dụng.
6. **EVE / AlphaMissense** – dự đoán biến thể gây bệnh không cần nhãn.
7. **PK/PD/ADME** + các bước khám phá thuốc + SAR.
8. **GNN message passing** + biểu diễn phân tử (SMILES/graph).
9. **GWAS + PRS** – cách tính, giới hạn (relative risk, đa dạng chủng tộc).
10. **XAI**: intrinsic vs post-hoc, 5 chiều đánh giá, SHAP/LIME, disagreement problem.
11. **-omics** & cancer subtyping/drug response.

## 💡 Mẹo làm bài
- Câu hỏi "so sánh" (X vs Y) rất hay ra → luyện các bảng so sánh trong mỗi file.
- Nhớ **1 ví dụ điển hình** cho mỗi khái niệm/mô hình (vd PopVAE cho population structure, Mutect2 cho somatic, EVE cho variant prediction).
- Với câu quy trình → **vẽ sơ đồ pipeline** kèm tên công cụ ở mỗi bước.
- Chú ý các con số hay hỏi: 3 tỷ bp, 23 cặp NST, 20 axit amin, ~20.000 gen, WES ≈ 1,4% WGS, start codon ATG, stop codon TAA/TAG/TGA, TI = TD50/ED50, small molecule < 900 Da.

**Chúc thi tốt! 🍀**
