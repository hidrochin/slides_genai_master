# Trắc nghiệm Chương 4 – Phân tích hệ gen (Genome Analysis + GATK)

> ⚠️ **Multiple-select: mỗi câu có 0→nhiều đáp án đúng.** ⭐ Chương trọng tâm nhất → nhiều câu & khó nhất.
> 🎚️ Độ khó: 🟢 TB · 🟠 Khó · 🔴 Rất khó. Giải thích trong khối **▸ Đáp án** dưới mỗi câu — tự làm trước khi mở.

---

## A. Nền tảng di truyền & giải trình tự

### Câu 1 · 🟠 Khó
Về **germline** vs **somatic** và **zygosity**:
- A. Germline có ở tế bào sinh dục, **truyền** cho đời sau, hiện diện ở **mọi** tế bào
- B. Somatic chỉ ở tập con tế bào (vd khối u), **không** truyền cho đời sau
- C. **Heterozygous** = biến thể ở **1** trong 2 NST; **Homozygous** = ở **cả 2**
- D. Đột biến ung thư (driver) thường là **germline**
- E. BRCA1/2 gây bệnh di truyền là ví dụ biến thể germline

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B, C, E** — đúng.
- ❌ **D** — sai: đột biến driver ung thư chủ yếu là **somatic** (dù một số hội chứng di truyền có germline predisposition).
</details>

---

### Câu 2 · 🔴 Rất khó
So sánh **công nghệ giải trình tự** & WGS/WES:
- A. Illumina: short read (50–150 bp), phổ biến, **độ chính xác cao** (lỗi thấp)
- B. PacBio (SMRT) & Nanopore: long read, **tỷ lệ lỗi cao hơn** Illumina
- C. Illumina có tỷ lệ lỗi **cao hơn** PacBio
- D. **Paired-end** giúp xử lý vùng lặp và gợi ý structural variant (khoảng cách cặp read bất thường)
- E. WES chỉ ~**1,4%** genome nhưng thường **coverage sâu hơn** ở vùng mã hóa
- F. Chromium 10x **đắt hơn** PacBio

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, D, E**

- ✅ **A, B, D, E** — đúng.
- ❌ **C** — sai: Illumina lỗi **thấp hơn** PacBio (đảo ngược).
- ❌ **F** — sai: Chromium 10x **rẻ hơn** PacBio (đắt hơn short read, rẻ hơn PacBio).
</details>

---

### Câu 3 · 🟢 TB
Về các **dự án hệ gen** & tài nguyên:
- A. HGP: 1990–2003, ~$3 tỷ, hoàn thành ~**92%** (8% còn lại rất khó)
- B. gnomAD (tiền thân **ExAC**) tổng hợp exome/genome
- C. DGV4VN/1KVG: WGS cho **1000 người Kinh** (Việt Nam)
- D. COSMIC = CSDL đột biến **soma** ung thư
- E. HGP đã hoàn thành **100%** ngay 2003

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: hoàn thành ~92%, phần còn lại (vùng lặp) rất khó (mãi sau mới bổ sung nhờ long-read).
</details>

---

## B. Định dạng dữ liệu & tiền xử lý

### Câu 4 · 🔴 Rất khó
Ghép **định dạng** & **CIGAR**:
- A. **FASTA** = trình tự đơn giản (reference, không cần quality score)
- B. **FASTQ** = trình tự + **Phred quality score**
- C. **GVCF** = có record cho **mọi vị trí** (kể cả không biến thể) → dùng multi-sample
- D. CIGAR: **M** = match, **I** = insertion, **D** = deletion, **S** = soft-clip
- E. Reference genome nên lưu ở **FASTQ** vì cần quality score
- F. **BAM** là dạng nén BGZF của SAM (~1/5 kích thước)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: reference dùng **FASTA** (authoritative, không cần quality). Bẫy FASTA↔FASTQ.
</details>

---

### Câu 5 · 🔴 Rất khó
Về **pipeline tiền xử lý GATK** & Read Group:
- A. Thứ tự đúng: **Map (BWA) → MarkDuplicates → BQSR**
- B. MarkDuplicates đánh dấu cặp read trùng do **PCR artifact** & sort theo tọa độ
- C. BQSR dùng **ML** sửa lỗi hệ thống base quality score, cần **known-sites (dbSNP)**
- D. **SM** (Sample) là tên cột mẫu trong VCF; **PU** được ưu tiên cho BQSR
- E. BQSR nên chạy **trước** khi map để tiết kiệm thời gian
- F. **LB** (library) được MarkDuplicates dùng để xác định duplicate

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: BQSR là bước **cuối** của tiền xử lý (sau map & markdup) — không thể chạy trước khi map. Bẫy thứ tự.
</details>

---

## C. Germline Variant Discovery

### Câu 6 · 🔴 Rất khó
**HaplotypeCaller** — chọn phát biểu ĐÚNG về 4 giai đoạn:
- A. (1) Xác định **active regions** (vùng có bằng chứng biến thể)
- B. (2) **Reassembly** bằng **De Bruijn-like graph**, realign bằng **Smith-Waterman**
- C. (3) Tính **likelihood** mỗi read với mỗi haplotype bằng **PairHMM**
- D. (4) Gán genotype bằng **Bayes' rule** (posterior)
- E. HaplotypeCaller loại bỏ duplicate bằng cách chạy lại PCR
- F. `-bamout` xuất BAM thể hiện realignment nội bộ (giải thích vì sao "thấy" biến thể)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: loại duplicate là việc của **MarkDuplicates** (bước tiền xử lý), không phải HaplotypeCaller.
</details>

---

### Câu 7 · 🔴 Rất khó
Về **GVCF workflow** & N+1 problem:
- A. Mỗi mẫu chạy HaplotypeCaller với `-ERC GVCF`
- B. **GenomicsDBImport** gộp GVCF; **GenotypeGVCFs** joint genotyping
- C. Giải quyết **N+1 problem** (thêm mẫu mới không cần chạy lại từ đầu)
- D. GATK4 dùng **GenomicsDBImport**; GATK3 dùng **CombineGVCFs**
- E. **GenotypeGVCFs** xuất **mọi** vị trí kể cả không biến thể ở tất cả mẫu
- F. Thấy bằng chứng ở nhiều mẫu → tăng tin cậy biến thể thật

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: **GenotypeGVCFs** chỉ xuất **site biến thể ở ≥1 mẫu** (không phải mọi vị trí; đó là đặc điểm của GVCF thô).
</details>

---

### Câu 8 · 🔴 Rất khó
Về **lọc biến thể germline** (callset refinement):
- A. **Hard filtering** dùng ngưỡng cứng: QD, FS, SOR, MQ, MQRankSum, ReadPosRankSum
- B. Ngưỡng kinh điển **QD < 2.0** → đánh dấu là biến thể chất lượng thấp
- C. **VQSR** học mô hình từ **truth set** (NA12878, HapMap...), tính **VQSLOD**, chạy trên **cohort**
- D. VQSR nên chạy **chung** SNP và INDEL trong một mô hình duy nhất
- E. **CNNScoreVariants** (deep learning): CNN_1D chỉ dùng annotation, CNN_2D dùng cả **read data**; tốt cho **single-sample**
- F. Hard filtering **luôn** tốt hơn VQSR trong mọi trường hợp

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B, C, E** — đúng (kể cả ngưỡng QD < 2.0).
- ❌ **D** — sai: VQSR chạy **riêng** SNP và INDEL (mỗi loại một mô hình). Bẫy hay gặp.
- ❌ **F** — sai: không "luôn"; VQSR cần cohort đủ lớn & truth set, hard filter dùng khi mẫu nhỏ.
</details>

---

### Câu 9 · 🟠 Khó
Về **đánh giá callset** & Ti/Tv:
- A. **Ti/Tv** = tỷ lệ transition/transversion
- B. **Transition** (A↔G, C↔T) **phổ biến hơn** transversion
- C. Ti/Tv lệch bất thường → dấu hiệu chất lượng callset kém
- D. **GATK VariantEval** so callset với dbSNP / truth set
- E. Transversion phổ biến hơn transition trong genome người

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: **transition** phổ biến hơn (đảo ngược).
</details>

---

## D. Somatic Variant Discovery

### Câu 10 · 🔴 Rất khó
Về **Mutect2** & tài nguyên somatic:
- A. Paradigm **Tumor–Normal pair** (khác germline joint calling)
- B. **PoN (Panel of Normals)**: loại **artifact kỹ thuật** & germline phổ biến ở mức quần thể
- C. **Matched normal**: mô thường CÙNG bệnh nhân → loại germline **đặc thù cá nhân**
- D. **Germline resource** (gnomAD af-only): lọc biến thể germline theo tần số quần thể
- E. Có thể chạy **tumor-only** khi không có normal
- F. PoN cho somatic **short variant** **giống hệt** PoN cho **CNV**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A, B, C, D, E** — đúng.
- ❌ **F** — sai: PoN cho CNV **khác hoàn toàn** (cần ≥10, khuyến nghị ≥40 normal có profile kỹ thuật gần). Bẫy hay gặp.
</details>

---

### Câu 11 · 🔴 Rất khó
Về **FilterMutectCalls** & CalculateContamination:
- A. **CalculateContamination** ước lượng cross-sample contamination
- B. **GetPileupSummaries** chạy trên **common germline variants (AF ≥ 1%)**
- C. Tìm site **HOM-VAR (ALT/ALT)** ở **Normal** → đo tỷ lệ read REF ở **Tumor** tại site đó
- D. **LearnReadOrientationModel** (từ **F1R2** counts) quan trọng cho mẫu **FFPE**
- E. FilterMutectCalls cần kết quả **GWAS** của bệnh nhân
- F. FilterMutectCalls kết hợp hard filter + statistical modeling, tối ưu **F-score**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: không dùng GWAS.
</details>

---

### Câu 12 · 🔴 Rất khó
Phân biệt **strand bias** và **orientation bias**:
- A. **Strand**: sợi forward (5'→3') vs reverse
- B. **Orientation (F/R)**: hướng read map vào reference
- C. **Strand bias**: bằng chứng ALT chỉ từ **1 strand** (toàn forward hoặc toàn reverse)
- D. **Orientation bias**: lỗi hóa học lúc **library prep** (vd G→T), quan trọng với **FFPE**; bằng chứng gần như toàn **F1R2** hoặc toàn **F2R1**
- E. **F1R2** = read1+read2 từ sợi forward; **F2R1** = từ sợi reverse
- F. Strand bias và orientation bias là **cùng một** hiện tượng

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A, B, C, D, E** — đúng.
- ❌ **F** — sai: là **hai hiện tượng khác nhau** (lệch theo sợi ↔ lệch theo hướng map/artifact hóa học).
</details>

---

### Câu 13 · 🔴 Rất khó
Về **Somatic CNV** & penalty λ:
- A. Đo **copy ratio** (proxy cho copy number), về bản chất là coverage & normalization
- B. Pipeline: PreprocessIntervals → CollectReadCounts → CreateReadCountPanelOfNormals → **DenoiseReadCounts** → **ModelSegments** → **CallCopyRatioSegments**
- C. **DenoiseReadCounts**: chuẩn hóa theo median PoN (log2) → denoise bằng **PCA** của PoN
- D. **Minor Allele Fraction** dùng site heterozygous để lộ **allelic imbalance**
- E. **penalty λ** điều khiển độ mượt segmentation: `Objective = Data fit + λ × (số segment)`; λ **thấp** → nhạy hơn (nhiều breakpoint)
- F. λ **không** ảnh hưởng số segment

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A, B, C, D, E** — đúng (λ thấp → nhạy, nhiều segment; λ cao → robust, ít segment).
- ❌ **F** — sai: λ **có** ảnh hưởng trực tiếp số segment (nó phạt số segment).
</details>

---

## E. Annotation & GenAI trong genomics

### Câu 14 · 🟠 Khó
Về **đột biến coding** & công cụ annotation:
- A. **Nonsense** = tạo stop codon sớm → protein cụt
- B. **Missense** = đổi 1 axit amin
- C. **Frameshift** = thêm/mất nucleotide **không** phải bội số 3 → lệch khung đọc
- D. **Funcotator, VEP, SnpEff, Annovar** là công cụ annotation
- E. **VarChat** là công cụ **GenAI** hỗ trợ diễn giải biến thể (tóm tắt y văn)
- F. **Missense** = tạo stop codon sớm làm cụt protein

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A, B, C, D, E** — đúng.
- ❌ **F** — sai: mô tả F là **nonsense**, không phải missense. Bẫy đảo nonsense↔missense.
</details>

---

### Câu 15 · 🔴 Rất khó
So sánh **EVE** và **AlphaMissense**:
- A. **EVE**: **Bayesian VAE**, học từ **MSA** (dữ liệu tiến hóa), **KHÔNG cần nhãn** (unsupervised)
- B. EVE tính **evolutionary index** → **GMM** phân biệt benign/pathogenic
- C. **AlphaMissense**: **fine-tune AlphaFold** (transformer, **KHÔNG** phải VAE), thêm **structural context**
- D. AlphaMissense mạnh hơn EVE trên ClinVar (auROC ~0.940 vs ~0.911)
- E. **Bayesian VAE**: weights là **phân phối** → cho ước lượng **bất định (uncertainty)**; train bằng **ELBO**
- F. Cả EVE và AlphaMissense đều là mô hình discriminative huấn luyện trên nhãn ClinVar

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A, B, C, D, E** — đúng.
- ❌ **F** — sai: EVE **không** dùng nhãn (unsupervised, học từ tiến hóa); ClinVar chỉ dùng để **đánh giá**. Bẫy "EVE dùng nhãn".
</details>

---

### Câu 16 · 🔴 Rất khó
Ghép **ứng dụng GenAI trong genomics** ↔ mô hình:
- A. **PopVAE** (VAE) → trực quan hóa **cấu trúc quần thể** (giữ global geometry, phản ánh di cư)
- B. **phyloGAN** (GAN + AliSim) → suy luận **cây phát sinh loài**; đo bằng **RF distance**
- C. **Artificial human genomes** → GAN, RBM, WGAN, CRBM; đánh giá overfitting bằng **AATS (<0.5 = overfit)**
- D. **AlphaFold** → sinh **cấu trúc protein 3D**
- E. **EVO** → **genomic foundation model 7B** tham số, đa mô thức DNA/RNA/protein
- F. **phyloGAN** dùng **VAE** để sinh cây

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A, B, C, D, E** — đúng.
- ❌ **F** — sai: phyloGAN dùng **GAN** (không phải VAE).
</details>

---

### Câu 17 · 🔴 Rất khó
Về mô hình sinh & quần thể học:
- A. **WGAN** dùng **Wasserstein distance** (ổn định hơn) + **Critic** (xuất điểm) thay Discriminator (xác suất 0–1)
- B. **RBM** có 2 lớp: **visible** & **hidden**
- C. **CNN** tốt cho bắt **motif / linkage disequilibrium** (cấu trúc cục bộ)
- D. **LD (Linkage Disequilibrium)**: allele ở locus gần nhau **không** kết hợp ngẫu nhiên
- E. **Imputation** = "điền" genotype thiếu dựa reference panel (vd 1000 Genomes)
- F. GAN dùng Wasserstein distance; WGAN dùng Jensen-Shannon divergence

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A, B, C, D, E** — đúng.
- ❌ **F** — sai: đảo ngược — **GAN dùng Jensen-Shannon**, **WGAN dùng Wasserstein**.
</details>

---

### Câu 18 · 🔴 Rất khó
Chọn **TẤT CẢ** phát biểu **SAI**:
- A. BQSR chạy trước MarkDuplicates để tối ưu
- B. CNNScoreVariants đặc biệt phù hợp cho **cohort lớn nhiều mẫu**
- C. EVE dùng nhãn ClinVar để huấn luyện có giám sát
- D. GenotypeGVCFs xuất mọi vị trí kể cả không biến thể
- E. Transversion phổ biến hơn transition trong genome người

<details><summary>▸ Đáp án</summary>

**SAI: A, B, C, D, E** (cả 5 đều sai — kiểu đề "bẫy tổng hợp")

- ❌ **A** — BQSR là bước **cuối** tiền xử lý.
- ❌ **B** — CNNScoreVariants tốt cho **single-sample**; VQSR mới cho cohort.
- ❌ **C** — EVE **unsupervised** (không dùng nhãn).
- ❌ **D** — GenotypeGVCFs chỉ xuất site **biến thể**.
- ❌ **E** — **transition** phổ biến hơn.
</details>
