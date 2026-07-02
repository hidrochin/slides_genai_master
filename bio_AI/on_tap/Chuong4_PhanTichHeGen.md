# Chương 4 – Phân tích hệ gen (Genome Analysis)

> Chương lớn nhất. Gồm: (A) Nền tảng di truyền học & công nghệ giải trình tự; (B) **Quy trình GATK** (tiền xử lý → germline → somatic → annotation); (C) **Ứng dụng GenAI trong phân tích hệ gen**.

---

## PHẦN A – NỀN TẢNG DI TRUYỀN & GIẢI TRÌNH TỰ

### 4.1. Germline vs Somatic ⭐
| | **Germline (dòng mầm)** | **Somatic (tế bào soma)** |
|---|---|---|
| Tế bào | Tế bào sinh dục (trứng, tinh trùng) | Mọi tế bào khác cơ thể |
| Di truyền | **Truyền cho đời sau** | **Không** truyền cho đời sau |
| Hiện diện | Có trong **mọi tế bào** cơ thể | Chỉ ở **một tập con** tế bào (vd khối u) |
| Ví dụ | Bệnh di truyền, BRCA1/2 | Đột biến ung thư (driver mutations) |

### 4.2. Biểu hiện gen & di truyền
- **Gene expression**: thông tin trong gen → chức năng (qua phiên mã RNA). Như "công tắc bật/tắt" + "núm điều chỉnh âm lượng".
- **Repressor**: protein ức chế biểu hiện gen (gắn vùng promoter, chặn tạo mRNA).
- **Genotype** (kiểu gen: BB, Bb, bb hoặc CC, CT, TT) vs **Phenotype** (kiểu hình).
- **Kiểu di truyền (family pedigree)**: Autosomal dominant (trội – mỗi thế hệ đều có), Autosomal recessive (lặn – cả bố mẹ mang gen), X-linked dominant/recessive, Y-linked, **Mitochondrial** (chỉ mẹ truyền).
- **BRCA1/BRCA2**: tumor suppressor, mất chức năng cả 2 copy → ung thư vú/buồng trứng.

### 4.3. Các loại biến thể di truyền (genetic variation) ⭐
- Khác biệt giữa 2 người: ~1 SNV mỗi 1000 bp → ~**2,7 triệu khác biệt (~0,1%)**. (Chính xác hơn: ~99,6% giống, ~0,4% khác khi tính cả indel).
- **Nhỏ (< 50 bp):**
  - **SNV/SNP** (Single Nucleotide Variant/Polymorphism) – biến thể 1 nucleotide.
  - **Indel** (Insertion/Deletion nhỏ).
- **Lớn (Structural Variants, SV):**
  - Indel > 50 bp, **CNV** (Copy Number Variation), **Inversion** (đảo đoạn), **Translocation** (chuyển đoạn), chromosomal fusion.
- **Mức NST**: Trisomy 21 (Down), 18 (Edwards), Turner, XYY.
- **Zygosity**: **heterozygous (het)** – 1 NST; **homozygous (hom)** – cả 2 NST.

### 4.4. Công nghệ giải trình tự (Sequencing Technologies) ⭐
| Công nghệ | Loại | Đặc điểm |
|---|---|---|
| **Illumina / BGI** | Short read (50–150 bp, tối đa 250) | Phổ biến nhất, shotgun, độ chính xác cao; khó với vùng lặp → dùng **paired-end** |
| **PacBio (SMRT)** | Long read (~50.000 bp) | Đọc dài, **tỷ lệ lỗi cao hơn** Illumina, đắt, cho nghiên cứu |
| **Nanopore (Oxford)** | Long read | DNA qua nanopore tạo dòng điện; đọc rất dài, thiết bị nhỏ (MinION); lỗi cao |
| **Chromium 10x** | Linked read (barcode) | Đắt hơn short read, rẻ hơn PacBio, chính xác hơn Nanopore |

- **NGS (Next-Generation Sequencing)**: massively parallel.
- **WGS (Whole-Genome Seq)**: toàn bộ ~3,1 tỷ bp; **WES (Whole-Exome Seq)**: chỉ ~**1,4%** genome (vùng mã hóa), coverage sâu hơn nhưng bỏ vùng non-coding.
- **Paired-end sequencing**: đọc 2 đầu mỗi fragment → 2 file FASTQ (R1, R2). Khoảng cách bất thường giữa cặp read → gợi ý deletion/insertion/translocation.

### 4.5. Các dự án hệ gen & tài nguyên
- **Human Genome Project (HGP)**: 1990–2003, 2500 nhà KH, 20 lab, 7 nước, ~**$3 tỷ**; hoàn thành ~92% (8% còn lại rất khó – vùng lặp).
- **1000 Genomes Project (1KGP)** (2008–2015); **HapMap** (bản đồ haplotype, **tag SNP**); **gnomAD** (tiền thân ExAC, tổng hợp exome/genome).
- **DGV4VN/1KVG**: dự án Việt Nam – giải trình tự WGS 30x cho **1000 người Kinh** → CSDL biến thể người Việt (VinBigdata, 2019–2023). Mục tiêu: reference panel cho **GWAS, PGx (dược lý gen), bệnh di truyền, xét nghiệm ADR**.
- **COSMIC** (đột biến soma ung thư), **TCGA** (Cancer Genome Atlas), **GDC portal**.

---

## PHẦN B – ⭐⭐ QUY TRÌNH GATK (GATK Best Practices)

### 4.6. Định dạng dữ liệu & công cụ
| Định dạng | Ý nghĩa |
|---|---|
| **FASTA** | Trình tự đơn giản (dùng cho **reference genome** – authoritative, không cần quality score) |
| **FASTQ** | Trình tự + **Phred quality score** (mã hóa ASCII); dữ liệu thô từ máy giải trình tự; file rất lớn (100s GB) |
| **SAM** | Sequence Alignment Map (read đã map vào reference) |
| **BAM** | SAM nén BGZF (~1/5 kích thước SAM) |
| **CRAM** | nén hơn nữa |
| **VCF** | Variant Call Format – kết quả gọi biến thể |
| **GVCF** | VCF có record cho **mọi vị trí** (kể cả không biến thể) – dùng cho multi-sample |

- **Reference genome**: chuỗi "chuẩn" của loài (mosaic từ ~20 người, chủ yếu RP11). Bản mới nhất **GRCh38** (2013), 24 chuỗi NST (22 + X + Y) + mtDNA.
- Công cụ pipeline: **GATK** (Broad Institute – chuẩn công nghiệp cho germline SNP/indel), **DRAGEN** (Illumina, tăng tốc phần cứng), **DRAGEN-GATK**, **NVIDIA Parabricks** (GPU, tăng tốc tới 107x).

### 4.7. Kiểm soát chất lượng (QC)
- **FastQC**: phân tích chất lượng FASTQ (per base quality, per sequence GC content, adapter content, duplication...). **MultiQC**: gộp báo cáo nhiều mẫu.
- **Fastp / Trimmomatic**: cắt/trim reads. **mosdepth**: tính độ sâu (depth/coverage).
- Chú ý: vùng **GC cao** thường coverage thấp hơn (artifact).

### 4.8. ⭐ Tiền xử lý dữ liệu (Data Pre-processing) – 3 bước
```
FASTQ → [1] Map to Reference → [2] Mark Duplicates → [3] Base Quality Score Recalibration (BQSR) → Analysis-ready BAM
```
1. **Map to Reference (BWA)**: ánh xạ từng cặp read vào reference. `bwa mem -t 7 -p reference.fasta reads.fq > mapped.sam`. ~360 triệu reads cho WGS 30x. Có thể song song hóa (`-t`).
   - **CIGAR string** trong SAM: **M** (match), **I** (insertion), **D** (deletion), **S** (soft-clip bỏ qua). Vd `1S4M1D2M1I1M`.
2. **Mark Duplicates** (MarkDuplicates / MarkDuplicatesSpark): đánh dấu các cặp read trùng do **PCR artifact** (khuếch đại) để downstream bỏ qua. Đồng thời **sort theo tọa độ**.
   - **Read Group (@RG)**: thông tin mẫu & lần chạy. Tag quan trọng: **ID** (unique, flowcell+lane), **PU** (Platform Unit, ưu tiên cho BQSR), **SM** (Sample – GATK gộp cùng SM là cùng mẫu; là tên cột trong VCF), **PL** (platform: ILLUMINA...), **LB** (library – MarkDuplicates dùng để xác định duplicate).
3. **BQSR (Base Quality Score Recalibration)**: dùng **ML** phát hiện & sửa lỗi hệ thống trong base quality score. Cần **known-sites** (vd **dbSNP**). Model đặc thù mỗi library/flowcell.
   ```
   gatk BaseRecalibrator -R ref.fasta -I markdups.bam --known-sites dbSNP.vcf -O recal.table
   gatk ApplyBQSR -R ref.fasta -I markdups.bam --bqsr-recal-file recal.table -O recal.bam
   ```

### 4.9. ⭐ Germline Short Variant Discovery (SNP + Indel)

**Nguồn lỗi cần kiểm soát**: PCR artifacts (duplicates), sequencing (base calling), alignment (misalignment), variant calling (low depth), genotyping.

#### HaplotypeCaller – 4 giai đoạn ⭐
1. **Define active regions**: vùng có bằng chứng biến thể (mismatch/gap).
2. **Reassembly**: xây **De Bruijn-like assembly graph** → liệt kê haplotype có thể; realign bằng **Smith-Waterman**.
3. **Likelihood**: **PairHMM** – pairwise alignment mỗi read với mỗi haplotype → ma trận likelihood.
4. **Assign genotypes**: áp dụng **Bayes' rule** → posterior probability mỗi genotype → gán genotype khả dĩ nhất.
- `-bamout`: xuất BAM thể hiện kết quả realignment nội bộ (giải thích vì sao HaplotypeCaller "thấy" biến thể mà BAM gốc không rõ).

#### Hai pipeline germline:
- **A. Single-sample**: HaplotypeCaller (default) → **Callset Refinement** = **CNNScoreVariants** (chấm điểm DL mỗi biến thể) → **FilterVariantTranches** (lọc theo SNP/INDEL sensitivity tranches).
- **B. Cohort (multi-sample) – GVCF workflow** ⭐:
  ```
  HaplotypeCaller (-ERC GVCF, mỗi mẫu) → GenomicsDBImport (gộp GVCF) → GenotypeGVCFs (joint genotyping) → VQSR
  ```
  - Giải quyết **N+1 problem** (thêm mẫu mới không cần chạy lại từ đầu – chỉ update GenomicsDB).
  - **GenotypeGVCFs**: chỉ xuất các site biến thể ở ≥1 mẫu.
  - Thấy bằng chứng ở nhiều mẫu → tăng tin cậy có biến thể thật.
  - GATK3 dùng **CombineGVCFs**; GATK4 dùng **GenomicsDBImport** (scale tốt hơn).

#### Callset Refinement – lọc biến thể (giảm False Positive)
Raw callset có nhiều FP → cần lọc. **3 cách:**
1. **Hard filtering**: lọc theo ngưỡng cứng trên các annotation:
   - **QD** (QualByDepth), **FS** (FisherStrand – strand bias, Fisher's exact test), **SOR** (StrandOddsRatio), **MQ** (Mapping Quality), **MQRankSum**, **ReadPosRankSum** (Wilcoxon rank-sum / Mann-Whitney U test), **ExcessHet**.
2. **VQSR (Variant Quality Score Recalibration)** ⭐: dùng **VariantRecalibrator** + **ApplyVQSR**. Học mô hình từ **truth set** (vd GiaB **NA12878**) để tính điểm **VQSLOD**. Làm việc trên **cohort/nhiều mẫu**.
3. **CNNScoreVariants** (deep learning): **CNN_1D** (chỉ dùng annotation) và **CNN_2D** (dùng cả **read data**). Tốt cho single-sample.
- **Genotype refinement**: **CalculateGenotypePosteriors** dùng **pedigree file** (thông tin gia đình/quần thể) để tinh chỉnh genotype.

#### Đánh giá callset (Callset Evaluation)
- **GATK VariantEval**; so với **dbSNP**, truth set.
- **Ti/Tv ratio** (Transition/Transversion): đột biến không ngẫu nhiên; **transition** (A↔G, C↔T) phổ biến hơn **transversion**. Ti/Tv lệch → dấu hiệu chất lượng.
- Cần khớp thuộc tính dataset (ethnicity, WGS/WES...).

### 4.10. ⭐ Somatic Variant Discovery (ung thư)

**Bối cảnh ung thư**: tế bào tích lũy đột biến → tăng sinh không kiểm soát → khối u → di căn (metastasis).
- **Driver mutations** (đột biến lái): trực tiếp thúc đẩy ung thư, được **chọn lọc dương**, tái diễn nhiều bệnh nhân → **trọng tâm phân tích**.
  - Oncogene (gain-of-function): KRAS, BRAF, EGFR. Tumor suppressor (loss-of-function): TP53, RB1, PTEN. Vd **BRAF V600E** (melanoma).
- **Passenger mutations** (đột biến hành khách): "đi ké", không gây bệnh.
- **Tumor heterogeneity** + **contamination** (mẫu u lẫn tế bào thường) → khó lấy mẫu → **dùng caller riêng cho somatic** (khác germline).
- Caller somatic: **Mutect2 (GATK)**, MuSE, VarScan2, Pindel, **DeepSomatic**.

#### Somatic SNV/Indel – pipeline (Mutect2) ⭐
Paradigm: **Tumor-Normal pair** (khác germline dùng joint calling).
- **2 tài nguyên quan trọng:**
  - **Panel of Normals (PoN)**: nhiều mẫu "normal" khỏe mạnh → loại **artifact kỹ thuật** & biến thể germline phổ biến ở mức quần thể.
  - **Germline Population Frequencies** (vd **gnomAD** af-only): tần số germline → lọc biến thể germline.
- **Matched Normal**: mô thường CÙNG bệnh nhân → loại germline đặc thù cá nhân.

**Tạo PoN (3 bước):**
```
Mutect2 (mỗi normal, --max-mnp-distance 0) → GenomicsDBImport (gộp) → CreateSomaticPanelOfNormals (--germline-resource gnomAD)
```
Quy tắc: giữ biến thể thấy ở **≥2 mẫu** nhưng dưới ngưỡng tần số germline.

**Gọi biến thể:**
```
gatk Mutect2 -R ref.fasta -I tumor.bam -I normal.bam -normal <SM_normal> \
  -pon pon.vcf.gz --germline-resource gnomad.vcf.gz \
  --f1r2-tar-gz f1r2.tar.gz -bamout tn.bam -O calls.vcf.gz
```
(Có chế độ **tumor-only** khi không có normal.)

**Lọc (FilterMutectCalls)** – kết hợp hard filter + statistical modeling, cần:
1. **CalculateContamination** – ước lượng **cross-sample contamination**:
   - **GetPileupSummaries** trên **common germline variants (AF ≥ 1%)** → tìm site **HOM-VAR (ALT/ALT)** ở Normal → đo tỷ lệ read REF ở Tumor tại các site đó → contamination rate (vd 1,15% ± 0,19%).
2. **LearnReadOrientationModel** (từ F1R2 counts) – mô hình **orientation bias** (quan trọng cho mẫu **FFPE**).
3. **FilterMutectCalls** – tính xác suất biến thể là somatic, tối ưu **F-score**.

**Strand bias vs Orientation bias** ⭐ (dễ hỏi):
- **Strand**: sợi forward (5'→3') vs reverse. **Orientation (F/R)**: hướng read map vào reference (F = cùng hướng ref, R = ngược).
- **F1R2** (read1+read2 từ sợi forward) vs **F2R1** (từ sợi reverse).
- **Strand bias**: bằng chứng ALT chỉ từ **1 strand** (toàn forward hoặc toàn reverse).
- **Orientation bias (read orientation artifact)**: lỗi hóa học lúc library prep (vd G→T), biểu hiện SNP allele fraction thấp mà bằng chứng gần như toàn F1R2 hoặc toàn F2R1.

**Annotation & xem kết quả**: **Funcotator** annotate somatic callset (vd tìm đột biến **TP53 chr17:7674220 C>T → p.R248Q missense**). Xem bằng **IGV** (locus TP53 chr17). Đối chiếu **AlphaMissense**.

#### Somatic CNV (Copy Number Variant) ⭐
- Đo **copy ratio** (tỷ lệ, proxy cho copy number) – **về coverage & normalization**.
- Gen thường **khuếch đại (amplified)**: HER2/ERBB2, EGFR, KIT, KRAS. Gen thường **mất (deleted)**: APC, BRCA1/2, PTEN, TP53, NF1/2.
- PoN cho CNV **hoàn toàn khác** PoN short variant (cần ≥10, khuyến nghị ≥40 normal có profile kỹ thuật gần).
- **Pipeline CNV:**
  ```
  PreprocessIntervals → CollectReadCounts → CreateReadCountPanelOfNormals →
  DenoiseReadCounts (standardize + denoise bằng PCA của PoN) →
  ModelSegments (Gaussian-kernel binary segmentation) → CallCopyRatioSegments (+/-/0)
  ```
  - **DenoiseReadCounts**: chuẩn hóa theo median PoN (log2 transform) → standardized CR → denoise bằng principal components → denoised CR.
  - **CallCopyRatioSegments**: đánh dấu **amplification (+), deletion (-), neutral (0)**.
  - **Minor Allele Fraction**: dùng site heterozygous để lộ **allelic imbalance** mà copy-ratio không thấy. CNV somatic làm lệch cân bằng allele 50:50.
  - **Penalty factor λ**: điều khiển độ mượt segmentation. `Objective = Data fit + λ × (số segment)`. λ thấp → nhạy hơn; λ cao → robust hơn.

### 4.11. ⭐ Functional Annotation (diễn giải biến thể)
- **Câu hỏi**: biến thể có ở vùng quan trọng (gene? UTR?)? Có đổi coding sequence? Có ảnh hưởng?
- **Công cụ**: **Funcotator** (GATK, output VCF/MAF, có data source germline & somatic, dùng gnomAD), **VEP** (Ensembl, tích hợp SIFT & PolyPhen), **SnpEff/SnpSift**, **Annovar**, PolyPhen.
- **Loại đột biến (coding):**
  - **Nonsense**: tạo stop codon sớm → protein cụt.
  - **Missense**: đổi 1 axit amin (có thể trung tính hoặc có hại).
  - **Frameshift**: thêm/mất nucleotide **không phải bội số 3** → lệch khung đọc.
- **Dự đoán pathogenicity**: CADD, **SIFT**, **PolyPhen-2**, REVEL, MutationAssessor, MetaLR.
- **VarChat**: công cụ **GenAI** đầu tiên hỗ trợ diễn giải biến thể – tìm & tóm tắt tài liệu khoa học (genetic assistant).

---

## PHẦN C – ⭐⭐ ỨNG DỤNG GenAI TRONG PHÂN TÍCH HỆ GEN

> Tham chiếu: Yelmen & Jay, *Deep Generative Models in Functional and Evolutionary Genomics*, Annual Review 2023.

### 4.12. Nền tảng mô hình sinh sâu (DGM)
- **VAE**: encoder → phân phối latent (regularized về N(0,1)) → decoder. Loss = reconstruction + KL. Sinh dữ liệu mới bằng cách lấy mẫu latent.
- **GAN**: generator vs discriminator/critic, huấn luyện đối kháng tới cân bằng. Có thể **conditional**.
- **RBM (Restricted Boltzmann Machine)**: 2 lớp (visible + hidden), học phân phối qua **Start → Reconstruct → Compare → Repeat** (contrastive divergence).
- **Kiến trúc NN**: Fully-connected (bắt mọi tương quan sequence), **CNN** (motif, linkage disequilibrium – cấu trúc cục bộ), **RNN** (dữ liệu tuần tự DNA/RNA).
- **WGAN vs GAN**: WGAN dùng **Wasserstein distance** (ổn định hơn, chống mode collapse) + **Critic** (xuất điểm số) thay Discriminator (xuất xác suất 0-1). GAN dùng Jensen-Shannon divergence (kém ổn định).

### 4.13. Năm ứng dụng GenAI (⭐ mỗi cái 1 ví dụ điển hình)

| # | Ứng dụng | Mô hình / Công cụ tiêu biểu | Ý chính |
|---|---|---|---|
| 1 | **Visualizing population structure** (trực quan cấu trúc quần thể) | **PopVAE** (VAE) | Giảm chiều tốt hơn PCA/t-SNE/UMAP; **giữ global geometry**, latent phản ánh **lịch sử di cư**; latent distance tương quan mạnh nhất với khoảng cách địa lý |
| 2 | **Phylogenetic inference** (suy luận cây phát sinh loài) | **phyloGAN** (GAN + AliSim simulator) | Generator sinh tree topology + branch length → simulator AliSim → CNN discriminator phân biệt real/fake. Đo bằng **RF distance** (Robinson-Foulds); tốt tới ~10 taxa |
| 3 | **Creating artificial human genomes** (tạo hệ gen nhân tạo) | **GAN, RBM, WGAN, CRBM** (Yelmen 2021/2023) | Giải quyết **privacy, data augmentation, đại diện quần thể**; tái tạo allele frequency, **LD**, population structure. Đánh giá overfitting bằng **AATS** (<0.5 overfit) |
| 4 | **Predicting disease variants** (dự đoán biến thể gây bệnh) | **EVE, AlphaMissense, EVO** | Xem 4.14 |
| 5 | **Generating protein structure** (sinh cấu trúc protein) | **AlphaFold (1/2/3), GENERALIST** | Dự đoán cấu trúc 3D từ trình tự |

**Khái niệm quần thể học cần nhớ:**
- **Population structure**: quần thể lớn chứa nhóm con có nền di truyền khác (do địa lý, văn hóa, sự kiện lịch sử). Quan trọng để tránh **confounding** trong GWAS.
- **Linkage Disequilibrium (LD)**: allele ở các locus gần nhau **không kết hợp ngẫu nhiên** – di truyền cùng nhau nhiều hơn kỳ vọng.
- **Allele frequency (AF)**, **Minor Allele Frequency (MAF)**.
- **Haplotype**: nhóm biến thể trên cùng NST di truyền cùng nhau.
- **Imputation**: "điền" genotype thiếu dựa vào reference panel (vd 1000 Genomes). AG nhân tạo cải thiện imputation ở MAF thấp.

### 4.14. ⭐ Dự đoán biến thể gây bệnh (chi tiết – hay hỏi)

**Vì sao cần?** ~98% biến thể (kể cả ở gene liên quan bệnh) chưa rõ hậu quả; số biến thể vượt xa khả năng thực nghiệm → cần dự đoán tính toán (**VUS – Variant of Unknown Significance**).

- **EVE (Evolutionary model of Variant Effect)** – Frazer 2021, Nature:
  - **Bayesian VAE** học phân phối biến đổi trình tự qua **MSA (Multiple Sequence Alignment)** của dữ liệu tiến hóa → **KHÔNG cần nhãn** (unsupervised).
  - Tính **evolutionary index** (≈ negative log-likelihood ratio variant vs wild-type) → **GMM (Gaussian Mixture Model)** phân biệt **benign vs pathogenic** (global-local mixture).
  - Dự đoán 36 triệu biến thể / 3.219 gene bệnh; vượt phương pháp dùng nhãn, ngang thực nghiệm.
  - **Bayesian VAE vs Standard VAE**: weights của NN là **phân phối** (không cố định) → cho **ước lượng bất định (uncertainty)**. Train bằng **ELBO**.
- **AlphaMissense** – Cheng 2023, Science:
  - **Fine-tune AlphaFold** (transformer, KHÔNG phải VAE) trên tần số biến thể người/linh trưởng → dự đoán mọi missense variant (likely benign/pathogenic/uncertain).
  - Mạnh hơn EVE (auROC 0.940 vs 0.911 ClinVar) nhờ **thêm structural context**.
- **EVO** – Nguyen 2024, Science: **genomic foundation model 7B params**, học từ 2,7 triệu genome prokaryote/phage; đa mô thức (DNA/RNA/protein), đa quy mô (molecule → genome).

**Kiến thức nền:**
- **Deep Mutational Scans (DMS) / MAVEs**: thực nghiệm đo hàng nghìn đột biến song song → thường dùng làm **ground truth**.
- **MSA (Multiple Sequence Alignment)**: căn chỉnh ≥3 trình tự để tìm vùng tương đồng → quan hệ tiến hóa/chức năng.

---

## 4.15. Câu hỏi ôn tập nhanh
1. Phân biệt **germline vs somatic**, **SNV/indel vs structural variant**. WGS vs WES?
2. So sánh **Illumina / PacBio / Nanopore**. Paired-end để làm gì?
3. Vẽ **pipeline tiền xử lý GATK** (3 bước). BQSR làm gì, cần gì?
4. Mô tả **4 giai đoạn HaplotypeCaller**. GVCF workflow giải quyết N+1 problem thế nào?
5. **VQSR vs CNNScoreVariants vs hard filtering** – khác nhau? VQSLOD?
6. **Mutect2**: vai trò **PoN**, **matched normal**, **germline resource**? Tumor-Normal paradigm?
7. Phân biệt **strand bias vs orientation bias**, **F1R2 vs F2R1**.
8. Pipeline **somatic CNV**: copy ratio, DenoiseReadCounts, ModelSegments, penalty λ?
9. Nonsense / missense / frameshift khác nhau? Công cụ annotation (Funcotator, VEP)?
10. **EVE vs AlphaMissense**: mô hình, dữ liệu, có/không dùng nhãn?
11. **PopVAE, phyloGAN, artificial genomes** – mô hình gì, giải quyết vấn đề gì?
12. **GAN vs WGAN**, **VAE vs Bayesian VAE**, **RBM/CRBM** hoạt động thế nào?
