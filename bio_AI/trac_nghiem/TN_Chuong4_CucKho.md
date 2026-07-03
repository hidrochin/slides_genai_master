# 🔥 ĐỀ CỰC KHÓ – CHƯƠNG 4 (GATK & Phân tích hệ gen)

> ⚠️ **Multiple-select: mỗi câu có 0→nhiều đáp án đúng.** Xét **từng phương án như câu Đúng/Sai độc lập**.
> 🎚️ Toàn bộ ở mức 🔥 **Cực khó** (vài câu 🔴 Rất khó): đọc trường VCF, giải mã CIGAR, cờ dòng lệnh GATK, tình huống lâm sàng, tính toán, và "chọn tất cả câu SAI".
> Dành cho ai đã nắm chắc [../on_tap/Chuong4_PhanTichHeGen.md](../on_tap/Chuong4_PhanTichHeGen.md). **Che đáp án, tự làm hết.**

---

### Câu 1 · 🔥 Cực khó
Một record VCF (single-sample, diploid) có:
`... DP=44; AC=1; AN=2; AF=0.500; ... GT=0/1`. Chọn phát biểu ĐÚNG:
- A. Mẫu này **dị hợp (heterozygous)** tại locus (GT = 0/1)
- B. **DP=44** là độ sâu đọc (số read) tại vị trí
- C. **AN=2** vì đây là sinh vật lưỡng bội (2 allele tại locus)
- D. **AC=1, AF=0.5** nghĩa là 1 trong 2 allele là ALT
- E. AF=0.500 chứng tỏ biến thể này có tần số 50% trong **quần thể người**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A–D** — đúng: GT 0/1 = het; AC/AN/AF ở single-sample là đếm allele **trong mẫu đó**.
- ❌ **E** — sai: AF ở đây là **allele frequency trong mẫu** (1/2=0.5), **không** phải tần số quần thể. Bẫy nhầm AF-mẫu ↔ AF-quần-thể (gnomAD).
</details>

---

### Câu 2 · 🔥 Cực khó
Vì sao dùng **QD (QualByDepth)** thay vì **QUAL** thô để lọc:
- A. **QUAL** bị "thổi phồng" theo độ sâu (depth-driven inflation) — site nhiều read → QUAL rất cao dù chưa chắc chất lượng thật
- B. **QD = QUAL chuẩn hóa theo độ sâu** → chỉ báo tin cậy ổn định hơn giữa các site
- C. Ngưỡng lọc kinh điển: **QD < 2.0** (đánh nhãn "QD2")
- D. Vì QD đã chuẩn hóa nên hai site có QUAL rất khác nhau vẫn có thể có QD tương đương
- E. QUAL cao **luôn** đồng nghĩa biến thể thật, nên QD là thừa

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A–D** — đúng (QUAL inflation theo depth là lý do cốt lõi dùng QD).
- ❌ **E** — sai: QUAL cao **không** đảm bảo biến thể thật (chính vì thế mới cần QD). Bẫy "luôn".
</details>

---

### Câu 3 · 🔥 Cực khó
Ghép **annotation** ↔ ý nghĩa (rank-sum & strand):
- A. **MQRankSum** = so **mapping quality (MAPQ)** của read mang REF vs read mang ALT
- B. **BaseQRankSum** = so **base quality** của REF vs ALT
- C. **ReadPosRankSum** = so **vị trí trong read** của allele (ALT dồn về đầu/cuối read = nghi ngờ)
- D. **FS (FisherStrand)** & **SOR (StrandOddsRatio)** = đo **strand bias**
- E. **MQ (RMSMappingQuality)** = trung bình cộng đơn giản của các MAPQ
- F. **ExcessHet** đo dư thừa dị hợp (dấu hiệu lỗi hệ thống)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: MQ là **root-mean-square (RMS)** của MAPQ, **không** phải trung bình cộng đơn giản. (RMS phạt nặng các MAPQ thấp.)
</details>

---

### Câu 4 · 🔥 Cực khó
Về **VQSR** (VariantRecalibrator + ApplyVQSR):
- A. Học mô hình (Gaussian mixture) trên annotation `-an QD -an MQ -an MQRankSum -an ReadPosRankSum -an FS -an SOR`
- B. Dùng **resource** như HapMap, Omni, 1000G, dbSNP (gắn cờ known/training/truth)
- C. Xuất **tranches file** ánh xạ mức **truth-sensitivity** (vd 99.9%, 99.0%, 90.0%) ↔ ngưỡng **VQSLOD**
- D. **VQSLOD** = log-odds một biến thể là thật vs artifact
- E. Nên chạy **chung** SNP và INDEL trong một lần cho tiện
- F. Đặt `--truth-sensitivity-filter-level 99.9` giữ độ nhạy cao (giữ nhiều biến thể thật, chấp nhận thêm FP)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: VQSR chạy **riêng** SNP và INDEL (đặc trưng annotation khác nhau). Bẫy hay gặp.
</details>

---

### Câu 5 · 🔥 Cực khó
Tình huống chọn **chiến lược lọc**: bạn có **1 mẫu WES** duy nhất (không có cohort), và một dự án khác có **cohort 2000 WGS**. Chọn ĐÚNG:
- A. Với 1 mẫu WES nhỏ → **hard filtering** hoặc **CNNScoreVariants** phù hợp hơn VQSR
- B. Với cohort 2000 WGS → **VQSR** phát huy tốt (đủ biến thể để học mô hình)
- C. **CNNScoreVariants** cần nhiều mẫu như VQSR mới chạy được
- D. **CNN_2D** dùng cả **read data** (không chỉ annotation) nên nhạy hơn CNN_1D với một số artifact
- E. Hard filtering **luôn** cho kết quả tốt hơn VQSR bất kể cỡ mẫu

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, D**

- ✅ **A, B, D** — đúng.
- ❌ **C** — sai: **CNNScoreVariants tốt cho single-sample** (không cần cohort như VQSR).
- ❌ **E** — sai: không "luôn"; VQSR mạnh hơn khi có cohort lớn + truth set.
</details>

---

### Câu 6 · 🔥 Cực khó
Về **HaplotypeCaller** — chi tiết nội bộ:
- A. **Active region** được xác định dựa bằng chứng mismatch/gap (bỏ qua vùng khớp reference hoàn toàn để tiết kiệm)
- B. **Reassembly**: dựng **De Bruijn-like graph** → liệt kê haplotype ứng viên; realign bằng **Smith-Waterman**
- C. **PairHMM** tính likelihood mỗi **read** với mỗi **haplotype**
- D. **Bayes' rule** cho posterior mỗi genotype → gán genotype khả dĩ nhất
- E. `-bamout` xuất BAM thể hiện **realignment nội bộ**, giúp giải thích vì sao HC "thấy" biến thể mà BAM gốc không rõ
- F. HaplotypeCaller gọi biến thể **từng vị trí độc lập** (position-by-position pileup) như phương pháp cũ

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A–E** — đúng.
- ❌ **F** — sai: HC dùng **local de-novo assembly** (haplotype-based), **KHÔNG** phải pileup từng vị trí. Đây là điểm khác biệt cốt lõi so với caller cũ (UnifiedGenotyper).
</details>

---

### Câu 7 · 🔥 Cực khó
Phân biệt **GVCF một mẫu** vs **đầu ra GenotypeGVCFs**:
- A. **GVCF một mẫu** (từ `-ERC GVCF`) có record cho **mọi vị trí**, gồm cả **non-variant blocks** (khối tham chiếu)
- B. Non-variant block giúp phân biệt "vị trí là homozygous-reference" với "vị trí không có dữ liệu"
- C. **GenotypeGVCFs** (sau joint) chỉ xuất **site biến thể ở ≥1 mẫu**
- D. Vì GVCF có mọi vị trí nên đầu ra GenotypeGVCFs cũng có mọi vị trí
- E. GenomicsDBImport (GATK4) scale tốt hơn CombineGVCFs (GATK3) khi số mẫu lớn

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B, C, E** — đúng (phân biệt C đúng vs D sai là điểm cực khó).
- ❌ **D** — sai: **GenotypeGVCFs lọc chỉ còn site biến thể** — không giữ mọi vị trí. Đừng suy diễn tuyến tính từ GVCF.
</details>

---

### Câu 8 · 🔥 Cực khó
Giải mã **CIGAR** `1S4M1D2M1I1M` (read vs reference):
- A. Read bị **soft-clip 1 base** ở đầu (không align nhưng vẫn nằm trong read)
- B. **Số base của read** tham gia = S+M+I = **9**
- C. **Độ dài đoạn tham chiếu (reference span)** = M+D = **8**
- D. **I (insertion)** tiêu tốn base của read nhưng **không** của reference; **D (deletion)** thì ngược lại
- E. Reference span và read length luôn bằng nhau vì read map 1-1 với reference

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- Đếm: M=4+2+1=7; I=1; D=1; S=1.
- ✅ **B** — read consumes M+I+S = 7+1+1 = **9**.
- ✅ **C** — reference span = M+D = 7+1 = **8**.
- ✅ **A, D** — đúng bản chất S/I/D.
- ❌ **E** — sai: I/D/S khiến read length ≠ reference span (chính là dấu hiệu indel/clip).
</details>

---

### Câu 9 · 🔥 Cực khó
Về **Read Group (@RG)** & tiền xử lý — chọn ĐÚNG:
- A. **PU (Platform Unit)** thường được **ưu tiên hơn ID** làm đơn vị hiệu chỉnh cho **BQSR**
- B. **SM (Sample)**: GATK gộp mọi read có cùng SM thành **một mẫu**; SM là tên cột trong VCF
- C. **LB (Library)**: **MarkDuplicates** dùng để xác định duplicate (duplicate cùng library mới có nghĩa)
- D. **BQSR** cần **known-sites** (dbSNP) để phân biệt mismatch "thật" (biến thể) với lỗi hệ thống
- E. Thứ tự đúng: **BQSR → Map → MarkDuplicates**
- F. Mô hình BQSR mang tính đặc thù mỗi **library/flowcell**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng (rất chi tiết nhưng đều chuẩn).
- ❌ **E** — sai: thứ tự là **Map → MarkDuplicates → BQSR** (BQSR cuối cùng).
</details>

---

### Câu 10 · 🔥 Cực khó
Về **Mutect2** & cờ dòng lệnh khi **tạo Panel of Normals**:
- A. Chạy Mutect2 trên **mỗi normal** với `--max-mnp-distance 0`
- B. `--max-mnp-distance 0` **tắt** khả năng gộp các biến thể liền kề thành MNP (để GenomicsDBImport gộp được)
- C. Sau đó: **GenomicsDBImport** → **CreateSomaticPanelOfNormals** (kèm `--germline-resource`)
- D. Quy tắc PoN short-variant: giữ biến thể thấy ở **≥2 mẫu** normal
- E. `--max-mnp-distance 0` để tăng độ nhạy phát hiện driver mutation trong tumor

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: cờ này liên quan **xây PoN từ normal** (tránh MNP làm hỏng gộp DB), **không** phải để tăng nhạy driver ở tumor. Bẫy gán sai mục đích.
</details>

---

### Câu 11 · 🔥 Cực khó
**Kịch bản CalculateContamination.** Chọn phát biểu ĐÚNG về cách ước lượng nhiễm chéo mẫu:
- A. **GetPileupSummaries** chạy trên **biallelic common variants (AF ≥ 1%)** ở cả tumor và normal
- B. Tìm site **HOM-VAR (ALT/ALT)** ở **Normal**
- C. Tại các site HOM-VAR đó, nếu **Tumor** lại xuất hiện nhiều read **REF** bất thường → dấu hiệu contamination
- D. **Càng nhiều read REF** tại site HOM-VAR (lẽ ra phải toàn ALT) → **contamination càng cao**
- E. Nên tìm HOM-VAR ở **Tumor** (không phải Normal) vì tumor sạch hơn
- F. Kết quả contamination được đưa vào **FilterMutectCalls**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng (logic: site lẽ ra toàn ALT mà lòi REF ⇒ có DNA lạ trộn vào).
- ❌ **E** — sai: tìm HOM-VAR ở **Normal** (dùng làm mốc), đo lệch ở **Tumor**. Đảo ngược tumor↔normal.
</details>

---

### Câu 12 · 🔥 Cực khó
Về **orientation bias** & LearnReadOrientationModel:
- A. Mutect2 xuất **F1R2 counts** qua `--f1r2-tar-gz f1r2.tar.gz`
- B. **LearnReadOrientationModel** dùng counts này học mô hình lỗi hướng đọc
- C. **Cực kỳ quan trọng** với mẫu **FFPE** (formalin cố định → lỗi hóa học vd C→T, G→T giả)
- D. Orientation bias biểu hiện: allele fraction thấp mà bằng chứng gần như **toàn F1R2** hoặc **toàn F2R1**
- E. Strand bias và orientation bias là cùng một chỉ số, chỉ khác tên
- F. **F1R2** = read1 forward + read2 reverse (theo quy ước sợi phát hiện allele)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: **hai hiện tượng khác nhau** (lệch theo sợi F/R vs artifact hóa học theo hướng đọc). Bẫy kinh điển.
</details>

---

### Câu 13 · 🔥 Cực khó
Về **Somatic CNV** — pipeline & bản chất:
- A. Thứ tự: PreprocessIntervals → CollectReadCounts → CreateReadCountPanelOfNormals → **DenoiseReadCounts** → **ModelSegments** → **CallCopyRatioSegments**
- B. **DenoiseReadCounts**: chuẩn hóa theo median PoN (log2) → **denoise bằng principal components (PCA)** của PoN → denoised copy ratio
- C. **ModelSegments** dùng segmentation (Gaussian-kernel) chia genome thành đoạn copy ratio đồng nhất
- D. **CallCopyRatioSegments** gắn nhãn **amplification (+) / deletion (−) / neutral (0)**
- E. **Minor Allele Fraction** (dùng site heterozygous) lộ **allelic imbalance** mà copy-ratio đơn thuần không thấy
- F. Copy ratio đo trực tiếp **số bản sao tuyệt đối**, không cần normalization

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A–E** — đúng.
- ❌ **F** — sai: copy ratio là **tỷ lệ** (proxy), **cần** normalization theo PoN; không đo số bản sao tuyệt đối trực tiếp.
</details>

---

### Câu 14 · 🔥 Cực khó
Về **penalty factor λ** trong segmentation CNV. `Objective = Data fit + λ × (số segment)`:
- A. **λ thấp** → phạt nhẹ số segment → segmentation **nhạy hơn** (nhiều breakpoint, dễ nhiễu)
- B. **λ cao** → phạt nặng số segment → **ít breakpoint** hơn, **robust** hơn (nhưng có thể bỏ sót CNV nhỏ)
- C. λ là tham số đánh đổi **độ khớp dữ liệu** ↔ **độ đơn giản (số đoạn)**
- D. λ không ảnh hưởng số segment
- E. Tăng λ vô hạn → mọi genome thành **một segment duy nhất**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B, C, E** — đúng (E là hệ quả logic: phạt cực nặng số segment → gộp hết).
- ❌ **D** — sai: λ **trực tiếp** điều khiển số segment.
</details>

---

### Câu 15 · 🔥 Cực khó
Về **PoN cho CNV** vs **PoN cho short variant**:
- A. **PoN CNV hoàn toàn khác** PoN short-variant về mục đích & cách xây
- B. PoN CNV cần **≥10** normal, **khuyến nghị ≥40** normal có **profile kỹ thuật gần** (cùng platform/panel)
- C. PoN CNV dùng để **denoise coverage** (loại nhiễu hệ thống theo profile), không phải để loại "biến thể germline phổ biến"
- D. PoN short-variant loại **artifact kỹ thuật + germline phổ biến** (giữ biến thể thấy ở ≥2 normal)
- E. Có thể dùng chung **một** PoN cho cả CNV lẫn short variant

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: **không** dùng chung — bản chất hai loại PoN khác nhau.
</details>

---

### Câu 16 · 🔥 Cực khó
Ghép **loại đột biến coding** với **hệ quả** — chọn ĐÚNG:
- A. **Nonsense**: đột biến điểm tạo **stop codon sớm** → protein cụt
- B. **Missense**: đổi 1 codon → 1 axit amin khác (có thể trung tính hoặc có hại)
- C. **Frameshift**: indel **không** bội số 3 → lệch khung đọc từ điểm đột biến trở đi
- D. Indel **đúng bội số 3** trong exon → thường **in-frame** (thêm/mất nguyên aa, ít nghiêm trọng hơn frameshift)
- E. **Funcotator, VEP, SnpEff, Annovar** annotate các hệ quả này; **SIFT/PolyPhen-2/CADD/REVEL** dự đoán pathogenicity
- F. Frameshift luôn ít nghiêm trọng hơn missense vì chỉ dịch chuyển khung

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A–E** — đúng.
- ❌ **F** — sai: **frameshift thường NGHIÊM TRỌNG hơn** (đổi toàn bộ downstream + hay tạo stop sớm). Bẫy đảo mức độ.
</details>

---

### Câu 17 · 🔥 Cực khó
So sánh **EVE** vs **AlphaMissense** — chọn ĐÚNG:
- A. **EVE**: Bayesian VAE, học **unsupervised** từ **MSA** (tiến hóa), **không cần nhãn** ClinVar
- B. EVE tính **evolutionary index** (≈ log-likelihood ratio variant vs wild-type) → **GMM** phân benign/pathogenic
- C. **AlphaMissense**: fine-tune **AlphaFold** (transformer) → thêm **structural context**; mạnh hơn EVE trên ClinVar (auROC ~0.940 vs ~0.911)
- D. **Bayesian VAE**: trọng số là **phân phối** → cho **uncertainty**; train bằng **ELBO**
- E. AlphaMissense là một **VAE** giống EVE
- F. Cả hai giải quyết vấn đề **VUS** (~98% biến thể chưa rõ hậu quả), vượt xa khả năng thực nghiệm

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: AlphaMissense **không** phải VAE — nó là **fine-tune AlphaFold (transformer)**. Bẫy gán sai kiến trúc.
</details>

---

### Câu 18 · 🔥 Cực khó
Ghép **ứng dụng GenAI genomics** ↔ mô hình & chỉ số đánh giá:
- A. **PopVAE** (VAE) → trực quan cấu trúc quần thể; giữ **global geometry** tốt hơn t-SNE/UMAP; latent tương quan **khoảng cách địa lý**
- B. **phyloGAN** (GAN + simulator **AliSim**) → suy cây phát sinh loài; đo bằng **RF distance (Robinson-Foulds)**
- C. **Artificial genomes** (GAN/RBM/WGAN/CRBM) → đánh giá overfitting bằng **AATS** (**< 0.5 = overfit**)
- D. **EVO** → genomic foundation model **7B tham số**, đa mô thức DNA/RNA/protein
- E. **phyloGAN** dùng discriminator để phân biệt cây thật/giả, nhưng bản chất là mô hình **VAE**
- F. **AlphaFold** → sinh cấu trúc protein 3D từ trình tự

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: phyloGAN là **GAN** (generator sinh topology + branch length; discriminator CNN), **không** phải VAE.
</details>

---

### Câu 19 · 🔥 Cực khó
Về mô hình sinh & quần thể học:
- A. **WGAN** dùng **Wasserstein distance** + **Critic** (xuất **điểm số**) thay Discriminator (xuất xác suất 0–1); ổn định hơn, chống mode collapse
- B. **GAN** dùng **Jensen-Shannon divergence** (kém ổn định hơn WGAN)
- C. **RBM/CRBM**: 2 lớp visible–hidden, học phân phối bằng **contrastive divergence**
- D. **CNN** phù hợp bắt **motif / linkage disequilibrium** (cấu trúc **cục bộ**); **RNN** cho chuỗi DNA/RNA tuần tự
- E. **Imputation** = "điền" genotype thiếu dựa **reference panel**; artificial genomes có thể cải thiện imputation ở **MAF thấp**
- F. **LD (Linkage Disequilibrium)** nghĩa là allele ở các locus gần nhau kết hợp **ngẫu nhiên**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E**

- ✅ **A–E** — đúng.
- ❌ **F** — sai: LD = **KHÔNG** kết hợp ngẫu nhiên (di truyền cùng nhau hơn kỳ vọng). Bẫy đảo nghĩa LD.
</details>

---

### Câu 20 · 🔴 Rất khó
Về **đánh giá callset** & Ti/Tv:
- A. **Ti/Tv** = transition / transversion
- B. **Transition** (A↔G, C↔T; đổi trong cùng nhóm purine/pyrimidine) **phổ biến hơn** transversion
- C. Ti/Tv lệch xa giá trị kỳ vọng (WGS ~2.0–2.1, WES ~3.0–3.3) → nghi callset nhiều FP
- D. **GATK VariantEval** so callset với **dbSNP** / truth set; cần khớp thuộc tính dataset (ethnicity, WGS/WES)
- E. Transversion phổ biến hơn transition

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng (Ti/Tv là "sanity check" chất lượng).
- ❌ **E** — sai: **transition** phổ biến hơn.
</details>

---

### Câu 21 · 🔥 Cực khó
Về **germline vs somatic** & lý do dùng caller riêng cho somatic:
- A. Somatic khó hơn: **tumor heterogeneity** + **tumor purity thấp** (u lẫn mô thường) → allele fraction biến thể **rất thấp**, biến thiên
- B. Germline: allele fraction kỳ vọng ~**0.5 (het)** hoặc **~1.0 (hom)** → caller giả định các mức rời rạc này
- C. Vì somatic AF thấp & liên tục nên **HaplotypeCaller (germline)** không phù hợp → dùng **Mutect2**
- D. Mutect2 dùng **joint calling nhiều mẫu** giống germline cohort
- E. Driver mutation somatic được **chọn lọc dương** & tái diễn nhiều bệnh nhân → trọng tâm phân tích

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B, C, E** — đúng (điểm cốt lõi: germline giả định AF rời rạc, somatic thì không).
- ❌ **D** — sai: Mutect2 dùng paradigm **Tumor–Normal pair** (không phải joint-calling cohort như GVCF germline).
</details>

---

### Câu 22 · 🔥 Cực khó
Về **reference genome** & định dạng:
- A. Reference là chuỗi "chuẩn" của loài, bản chất là **mosaic** từ nhiều cá thể (chủ yếu 1 donor RP11)
- B. **GRCh38** là bản mới (24 chuỗi NST: 22 + X + Y) + mtDNA
- C. Reference lưu ở **FASTA** (không cần Phred quality score)
- D. **FASTQ** thô từ máy giải trình tự có kèm **Phred quality** (mã ASCII), file rất lớn
- E. **BAM** = SAM ở dạng văn bản, kích thước lớn hơn SAM
- F. **CRAM** nén cao hơn BAM

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: **BAM là bản NÉN (BGZF) nhị phân** của SAM (~1/5 kích thước), **không** phải văn bản lớn hơn.
</details>

---

### Câu 23 · 🔴 Rất khó
Về **công nghệ giải trình tự** & WGS/WES (số liệu):
- A. Illumina: short read **50–150 bp** (tối đa ~250), lỗi thấp, phổ biến nhất
- B. PacBio (SMRT) & Nanopore: long read, **lỗi cao hơn** Illumina
- C. **WGS ~3,1 tỷ bp**; **WES ~1,4%** genome (vùng exon), coverage sâu hơn nhưng bỏ non-coding
- D. **Paired-end**: đọc 2 đầu fragment (R1, R2); khoảng cách cặp bất thường → gợi ý SV
- E. Nanopore lỗi **thấp hơn** Illumina nhờ đọc dài

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: Nanopore lỗi **cao hơn** Illumina (đọc dài đánh đổi độ chính xác).
</details>

---

### Câu 24 · 🔥 Cực khó
**Kịch bản diễn giải Mutect2 output.** Một SNV trong tumor: allele fraction ~3%, absent ở matched normal, **không** trong gnomAD, bằng chứng ALT cân bằng F1R2/F2R1, QUAL & depth tốt, nằm ở **TP53 chr17** gây **p.R248Q (missense)**. Chọn ĐÚNG:
- A. Đây là **ứng viên somatic thật đáng tin** (qua các bộ lọc: không germline, không orientation bias)
- B. AF thấp ~3% **không** loại trừ somatic thật (tumor purity/heterogeneity làm AF thấp)
- C. Vì cân bằng F1R2/F2R1 → **không** phải orientation artifact
- D. TP53 là tumor suppressor; missense R248Q là **hotspot** có thể mất chức năng
- E. AF chỉ 3% nên **chắc chắn** là sequencing error, phải loại

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng: đây đúng là kiểu ứng viên somatic thật (dùng **Funcotator** annotate, xem **IGV**, đối chiếu **AlphaMissense**).
- ❌ **E** — sai: AF thấp là **bình thường** với somatic; không thể kết luận "chắc chắn error". Bẫy "chắc chắn".
</details>

---

### Câu 25 · 🔥 Cực khó
**Chọn TẤT CẢ phát biểu SAI** (bẫy tổng hợp GATK):
- A. Thứ tự tiền xử lý: BQSR → Map → MarkDuplicates
- B. GenotypeGVCFs xuất mọi vị trí kể cả non-variant
- C. VQSR chạy chung SNP và INDEL trong một mô hình
- D. CNNScoreVariants cần cohort lớn như VQSR
- E. Tại site HOM-VAR, tìm ở **Tumor** để ước lượng contamination
- F. EVE là mô hình discriminative huấn luyện trực tiếp trên nhãn ClinVar

<details><summary>▸ Đáp án</summary>

**SAI: A, B, C, D, E, F (cả 6)**

- ❌ A: Map → MarkDuplicates → **BQSR**.
- ❌ B: GenotypeGVCFs chỉ xuất **site biến thể ≥1 mẫu** (GVCF một mẫu mới có non-variant blocks).
- ❌ C: VQSR chạy **riêng** SNP/INDEL.
- ❌ D: CNNScoreVariants tốt cho **single-sample**.
- ❌ E: tìm HOM-VAR ở **Normal**, đo lệch ở Tumor.
- ❌ F: EVE **unsupervised** (không dùng nhãn; ClinVar chỉ để đánh giá).

> 🎯 6 câu SAI này gom đúng **6 bẫy chết người** của Chương 4. Nhận ra hết ⇒ bạn nắm chắc phần lõi GATK.
</details>

---

### Câu 26 · 🔥 Cực khó
Về **hai pipeline germline** & công cụ tinh chỉnh genotype:
- A. **Single-sample**: HaplotypeCaller → **CNNScoreVariants** → **FilterVariantTranches**
- B. **Cohort**: HaplotypeCaller (`-ERC GVCF`) → GenomicsDBImport → GenotypeGVCFs → **VQSR**
- C. **CalculateGenotypePosteriors** dùng **pedigree file** (gia đình/quần thể) để tinh chỉnh genotype (genotype refinement)
- D. **FilterVariantTranches** lọc theo **SNP/INDEL sensitivity tranches** (dùng với điểm CNN)
- E. Genotype refinement bằng pedigree chỉ áp dụng cho **somatic** (Mutect2)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: pedigree/genotype refinement là của **germline** (di truyền gia đình), **không** dùng cho somatic (somatic không di truyền).
</details>

---

## 📊 Bản đồ chủ đề (tra sau khi làm)

| Cụm | Câu |
|---|---|
| VCF fields / annotation / QD / rank-sum | 1, 2, 3 |
| VQSR / CNN / hard filter / tranches | 4, 5, 26 |
| HaplotypeCaller / GVCF / joint / CIGAR / @RG | 6, 7, 8, 9 |
| Mutect2 / PoN / contamination / orientation bias | 10, 11, 12, 24 |
| CNV / λ / PoN-CNV | 13, 14, 15 |
| Annotation / EVE / AlphaMissense | 16, 17 |
| GenAI apps / WGAN/RBM / population genetics | 18, 19 |
| Ti/Tv / germline-somatic / reference / sequencing | 20, 21, 22, 23 |
| Bẫy tổng hợp "chọn tất cả câu SAI" | 25 |

**Tự chấm:** mỗi câu chỉ đúng khi chọn **chính xác toàn bộ** phương án đúng. Đây là đề khó nhất bộ — đúng ≥18/26 là rất tốt; dưới 13/26 nên đọc lại kỹ Phần B của [../on_tap/Chuong4_PhanTichHeGen.md](../on_tap/Chuong4_PhanTichHeGen.md).
