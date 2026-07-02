# Trắc nghiệm Chương 4 – Phân tích hệ gen (Genome Analysis + GATK)

> ⚠️ **Nhiều đáp án đúng có thể xảy ra.** Đây là chương trọng tâm nhất → nhiều câu nhất. Tự làm rồi so với **ĐÁP ÁN** ở cuối file.

---

### A. Nền tảng di truyền & giải trình tự

**Câu 1.** Phân biệt **germline** và **somatic**?
- A. Germline có ở tế bào sinh dục (trứng, tinh trùng)
- B. Germline được truyền cho đời sau
- C. Somatic chỉ ở một tập con tế bào (vd khối u)
- D. Somatic được truyền cho đời sau
- E. Germline variant có trong mọi tế bào cơ thể
- F. Đột biến somatic không truyền cho con cái

**Câu 2.** Về **biến thể di truyền**, phân loại ĐÚNG?
- A. SNV/SNP = biến thể 1 nucleotide (nhỏ, < 50 bp)
- B. Indel = thêm/mất nhỏ
- C. CNV, inversion, translocation = structural variant (lớn)
- D. Heterozygous = biến thể ở cả 2 nhiễm sắc thể
- E. Homozygous = biến thể ở cả 2 nhiễm sắc thể
- F. Hai người khác nhau ~1 SNV mỗi 1000 bp (~2,7 triệu khác biệt)

**Câu 3.** So sánh các **công nghệ giải trình tự**?
- A. Illumina = short read (50–150 bp), phổ biến nhất
- B. PacBio (SMRT) = long read (~50.000 bp), tỷ lệ lỗi cao hơn Illumina
- C. Nanopore = long read, thiết bị nhỏ (MinION), lỗi cao
- D. Illumina có tỷ lệ lỗi cao hơn PacBio
- E. Paired-end giúp align vùng lặp và phát hiện structural variant
- F. Chromium 10x đắt hơn PacBio

**Câu 4.** So sánh **WGS** và **WES**?
- A. WGS = giải trình tự toàn bộ genome (~3,1 tỷ bp)
- B. WES = chỉ vùng exome (~1,4% genome)
- C. WES cho coverage sâu hơn ở vùng mã hóa
- D. WES bỏ sót vùng non-coding (promoter, intron, enhancer)
- E. WGS chỉ giải trình tự vùng mã hóa

**Câu 5.** Về các **dự án hệ gen** và tài nguyên?
- A. Human Genome Project (1990–2003, ~$3 tỷ)
- B. gnomAD (tiền thân ExAC) tổng hợp dữ liệu exome/genome
- C. DGV4VN/1KVG giải trình tự WGS cho 1000 người Kinh (Việt Nam)
- D. COSMIC là CSDL đột biến soma ung thư
- E. HapMap là bản đồ haplotype với tag SNP
- F. HGP đã hoàn thành 100% ngay từ 2003

---

### B. Định dạng dữ liệu & tiền xử lý GATK

**Câu 6.** Ghép đúng **định dạng dữ liệu**?
- A. FASTA = trình tự đơn giản (dùng cho reference genome)
- B. FASTQ = trình tự + Phred quality score
- C. BAM = SAM nén (~1/5 kích thước)
- D. VCF = Variant Call Format
- E. GVCF = VCF có record cho mọi vị trí (dùng multi-sample)
- F. FASTQ dùng cho reference vì không cần quality score

**Câu 7.** Về **CIGAR string** trong SAM?
- A. M = matching position
- B. I = insertion gap
- C. D = deletion gap
- D. S = soft-clipped (bỏ qua)
- E. M = mismatch bắt buộc

**Câu 8.** Thứ tự ĐÚNG của **pipeline tiền xử lý GATK**?
- A. Map to Reference (BWA) → Mark Duplicates → BQSR
- B. BQSR → Map to Reference → Mark Duplicates
- C. Mark Duplicates loại bỏ cặp read trùng do PCR artifact
- D. BQSR dùng ML sửa lỗi hệ thống trong base quality score
- E. BQSR cần known-sites (vd dbSNP)
- F. Mark Duplicates diễn ra trước khi map

**Câu 9.** Về **Read Group (@RG)**?
- A. ID = định danh unique (flowcell + lane)
- B. SM = Sample (GATK gộp cùng SM là cùng mẫu)
- C. PL = platform (ILLUMINA...)
- D. LB = library (MarkDuplicates dùng để xác định duplicate)
- E. SM là tên cột trong file VCF
- F. ID luôn được ưu tiên hơn PU cho base recalibration

---

### C. Germline Variant Discovery

**Câu 10.** **HaplotypeCaller** hoạt động qua 4 giai đoạn nào?
- A. Define active regions (vùng có bằng chứng biến thể)
- B. Reassembly bằng De Bruijn-like assembly graph
- C. Tính likelihood haplotype bằng PairHMM
- D. Assign genotypes bằng Bayes' rule
- E. Realign haplotype bằng thuật toán Smith-Waterman
- F. Loại bỏ duplicate bằng PCR

**Câu 11.** Về **GVCF workflow** (cohort/multi-sample)?
- A. HaplotypeCaller chạy với `-ERC GVCF` cho mỗi mẫu
- B. GenomicsDBImport gộp các GVCF
- C. GenotypeGVCFs thực hiện joint genotyping
- D. Giải quyết N+1 problem (thêm mẫu không cần chạy lại từ đầu)
- E. GATK4 dùng GenomicsDBImport, GATK3 dùng CombineGVCFs
- F. GenotypeGVCFs xuất mọi vị trí kể cả không biến thể

**Câu 12.** Các cách **lọc biến thể germline** (callset refinement)?
- A. Hard filtering (ngưỡng cứng: QD, FS, SOR, MQ, ReadPosRankSum)
- B. VQSR (dùng ML trên cohort, tính điểm VQSLOD)
- C. CNNScoreVariants (deep learning, tốt cho single-sample)
- D. CNN_2D dùng cả read data trong chấm điểm
- E. VQSR học từ truth set (vd GiaB NA12878)
- F. Hard filtering luôn tốt hơn VQSR trong mọi trường hợp

**Câu 13.** Về **đánh giá callset** (evaluation)?
- A. Ti/Tv = tỷ lệ transition/transversion
- B. Transition (A↔G, C↔T) phổ biến hơn transversion
- C. GATK VariantEval là công cụ đánh giá
- D. So sánh với dbSNP và truth set
- E. Transversion phổ biến hơn transition trong genome người

---

### D. Somatic Variant Discovery

**Câu 14.** Về **driver mutations** và **passenger mutations**?
- A. Driver mutation trực tiếp thúc đẩy ung thư
- B. Driver được chọn lọc dương, tái diễn nhiều bệnh nhân
- C. Passenger "đi ké", không gây bệnh
- D. Oncogene (gain-of-function): KRAS, BRAF, EGFR
- E. Tumor suppressor (loss-of-function): TP53, RB1, PTEN
- F. Passenger mutation là trọng tâm phân tích somatic

**Câu 15.** Về pipeline **Mutect2** (somatic SNV/Indel)?
- A. Dùng paradigm Tumor-Normal pair
- B. Panel of Normals (PoN) loại artifact kỹ thuật & germline phổ biến
- C. Matched normal loại germline đặc thù cá nhân
- D. Germline resource (gnomAD) giúp lọc biến thể germline
- E. Có thể chạy tumor-only khi không có normal
- F. PoN cho somatic SNV giống hệt PoN cho CNV

**Câu 16.** **FilterMutectCalls** cần các đầu vào nào?
- A. Ước lượng cross-sample contamination (CalculateContamination)
- B. Read orientation model (LearnReadOrientationModel từ F1R2)
- C. Tumor segmentation
- D. Germline population frequencies
- E. Kết quả GWAS của bệnh nhân

**Câu 17.** Phân biệt **strand bias** và **orientation bias**?
- A. Strand: sợi forward vs reverse
- B. Orientation (F/R): hướng read map vào reference
- C. Strand bias: bằng chứng ALT chỉ từ 1 strand (toàn forward/reverse)
- D. Orientation bias: lỗi hóa học lúc library prep (vd G→T), quan trọng với mẫu FFPE
- E. F1R2 = read1+read2 từ sợi forward; F2R1 = từ sợi reverse
- F. Strand bias và orientation bias là cùng một hiện tượng

**Câu 18.** Về **Somatic CNV**?
- A. Đo copy ratio (proxy cho copy number)
- B. Gen thường khuếch đại: HER2/ERBB2, EGFR, KRAS
- C. Gen thường mất: BRCA1/2, PTEN, TP53, APC
- D. PoN cho CNV cần ≥10, khuyến nghị ≥40 normal
- E. DenoiseReadCounts chuẩn hóa bằng median PoN + PCA
- F. PoN cho CNV giống PoN cho short variant

**Câu 19.** Về **penalty factor λ** trong segmentation CNV?
- A. Điều khiển độ mượt của segmentation
- B. λ thấp → tăng độ nhạy (nhiều breakpoint hơn)
- C. λ cao → tăng độ robust (ít breakpoint hơn)
- D. Objective = Data fit + λ × (số segment)
- E. λ không ảnh hưởng đến số segment

---

### E. Annotation & GenAI trong genomics

**Câu 20.** Phân loại **đột biến coding** và công cụ annotation?
- A. Nonsense = tạo stop codon sớm → protein cụt
- B. Missense = đổi 1 axit amin
- C. Frameshift = thêm/mất nucleotide không phải bội số 3
- D. Funcotator và VEP là công cụ annotation
- E. VarChat là công cụ GenAI hỗ trợ diễn giải biến thể
- F. Missense = tạo stop codon sớm

**Câu 21.** So sánh **EVE** và **AlphaMissense**?
- A. EVE dùng Bayesian VAE, học từ MSA, KHÔNG cần nhãn
- B. AlphaMissense fine-tune AlphaFold (transformer), thêm structural context
- C. EVE tính evolutionary index → GMM phân biệt benign/pathogenic
- D. AlphaMissense mạnh hơn EVE trên ClinVar (auROC 0.940 vs 0.911)
- E. Cả hai đều là mô hình phân biệt (discriminative) dùng nhãn ClinVar
- F. Bayesian VAE cho ước lượng bất định (uncertainty)

**Câu 22.** Ghép đúng **ứng dụng GenAI** với mô hình?
- A. PopVAE (VAE) = trực quan hóa cấu trúc quần thể
- B. phyloGAN (GAN + AliSim) = suy luận cây phát sinh loài
- C. Artificial genomes = GAN, RBM, WGAN, CRBM
- D. AlphaFold = sinh cấu trúc protein
- E. EVO = genomic foundation model 7B tham số
- F. phyloGAN dùng VAE để sinh cây

**Câu 23.** Về các mô hình sinh trong genomics?
- A. WGAN dùng Wasserstein distance (ổn định hơn GAN)
- B. WGAN dùng Critic (xuất điểm số) thay Discriminator (xuất xác suất 0-1)
- C. RBM có 2 lớp: visible và hidden
- D. CNN tốt cho bắt motif/linkage disequilibrium (cấu trúc cục bộ)
- E. AATS < 0.5 chỉ ra overfitting của artificial genomes
- F. GAN dùng Wasserstein distance, WGAN dùng Jensen-Shannon divergence

**Câu 24.** Về khái niệm quần thể học (population genetics)?
- A. Linkage Disequilibrium (LD): allele ở locus gần nhau không kết hợp ngẫu nhiên
- B. Haplotype: nhóm biến thể trên cùng NST di truyền cùng nhau
- C. MAF = Minor Allele Frequency
- D. Population structure quan trọng để tránh confounding trong GWAS
- E. Imputation = "điền" genotype thiếu dựa vào reference panel
- F. LD nghĩa là các allele luôn kết hợp ngẫu nhiên

---

## ✅ ĐÁP ÁN & GIẢI THÍCH

**1: A, B, C, E, F** — D sai (somatic *không* truyền cho đời sau).
**2: A, B, C, E, F** — D sai: heterozygous = biến thể ở **1** NST (không phải cả 2); homozygous mới ở cả 2 NST (đáp án E).
**3: A, B, C, E** — D sai (Illumina lỗi *thấp* hơn PacBio); F sai (Chromium 10x *rẻ* hơn PacBio).
**4: A, B, C, D** — E sai (WGS giải trình tự *toàn bộ*, không chỉ vùng mã hóa).
**5: A, B, C, D, E** — F sai (HGP hoàn thành ~92%, 8% còn lại rất khó).
**6: A, B, C, D, E** — F sai (reference dùng *FASTA*, không phải FASTQ).
**7: A, B, C, D** — E sai (M là *match*, không phải mismatch bắt buộc).
**8: A, C, D, E** — B, F sai thứ tự (map trước, duplicate sau).
**9: A, B, C, D, E** — F sai (PU *ưu tiên hơn* ID cho base recalibration).
**10: A, B, C, D, E** — F không phải giai đoạn của HaplotypeCaller.
**11: A, B, C, D, E** — F sai (GenotypeGVCFs chỉ xuất site *biến thể* ở ≥1 mẫu).
**12: A, B, C, D, E** — F sai (không phải luôn tốt hơn; VQSR tốt cho cohort lớn).
**13: A, B, C, D** — E sai (transition *phổ biến hơn* transversion).
**14: A, B, C, D, E** — F sai (driver mới là trọng tâm, không phải passenger).
**15: A, B, C, D, E** — F sai (PoN somatic SNV *khác hoàn toàn* PoN cho CNV).
**16: A, B, C, D** — E sai (không dùng GWAS).
**17: A, B, C, D, E** — F sai (là 2 hiện tượng *khác nhau*).
**18: A, B, C, D, E** — F sai (PoN CNV *khác* PoN short variant).
**19: A, B, C, D** — E sai (λ có ảnh hưởng đến số segment).
**20: A, B, C, D, E** — F sai (missense = đổi aa, không phải stop codon; đó là nonsense).
**21: A, B, C, D, F** — E sai (EVE là generative *không* dùng nhãn; AlphaMissense dùng weak labels nhưng không phải "cả hai discriminative dùng ClinVar").
**22: A, B, C, D, E** — F sai (phyloGAN dùng *GAN*, không phải VAE).
**23: A, B, C, D, E** — F sai (đảo ngược: GAN dùng Jensen-Shannon, WGAN dùng Wasserstein).
**24: A, B, C, D, E** — F sai (LD nghĩa là *không* kết hợp ngẫu nhiên).
