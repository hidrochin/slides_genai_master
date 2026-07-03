# 🏁 ĐỀ TỔNG HỢP 50 CÂU – Mix 6 chương (IT5428)

> ⚠️ **Multiple-select: mỗi câu có 0→nhiều đáp án đúng.** Xét **từng phương án như câu Đúng/Sai độc lập**.
> 🎚️ Độ khó: 🟠 Khó · 🔴 Rất khó · 🔥 **Cực khó** (liên chương / tình huống / tính toán / "chọn tất cả câu SAI").
> Câu bị **xáo trộn chương** như thi thật. Giải thích trong khối `▸ Đáp án` (có ghi chương ở cuối để tra cứu). **Che đáp án, tự làm hết trước.**
>
> Tài liệu gốc: [../on_tap/](../on_tap/) (đã gắn nhãn 🔴/🟡/⚪ + mục "Điểm tủ").

---

### Câu 1 · 🔴 Rất khó
Về mô hình **discriminative** vs **generative**:
- A. Discriminative học `P(Y|X)`; generative học `P(X)` hoặc `P(X,Y)`
- B. Từ generative có thể suy ra classifier qua Bayes: `P(Y|X) ∝ P(X|Y)P(Y)`
- C. Generative luôn được huấn luyện có giám sát
- D. VAE, GAN là generative; hồi quy logistic là discriminative
- E. Chỉ generative mới có khả năng lấy mẫu sinh dữ liệu mới

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, D, E** — C sai: generative thường **không giám sát** (học `P(X)`). *(Ch1)*
</details>

---

### Câu 2 · 🔥 Cực khó
Một mRNA trưởng thành có ORF bắt đầu ATG, sau đó **17 codon mã hóa axit amin**, rồi một stop codon. Chọn phát biểu ĐÚNG:
- A. Chiều dài ORF (kể cả start & stop) = **57 nucleotide**
- B. ORF này mã hóa **18 axit amin** (kể cả Methionine mở đầu)
- C. Stop codon là một trong TAA/TAG/TGA và **không** mã hóa axit amin
- D. Vùng ORF có tổng cộng **19 codon**
- E. Vì có 17 codon giữa nên chiều dài ORF phải là bội số của 17

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- Đếm codon: **1 start + 17 giữa + 1 stop = 19 codon**.
- ✅ **A** — 19 codon × 3 = **57 nt**.
- ✅ **B** — start (ATG=Met) + 17 = **18 aa** (stop không tính aa).
- ✅ **C** — đúng.
- ✅ **D** — **19 codon** là đúng → **không loại D theo cảm tính**. Đây chính là bẫy: nhiều người thấy "19" lạ mắt nên bỏ, dẫn tới thiếu đáp án.
- ❌ **E** — sai: ORF là bội số của **3**, không phải 17.

> ⚠️ Câu này rèn thói quen **đếm lại và chọn đủ** (multiple-select chỉ đúng khi chọn *chính xác toàn bộ*). *(Ch2)*
</details>

---

### Câu 3 · 🔴 Rất khó
Thuốc X có **TD50 = 300 mg**, **ED50 = 150 mg**; thuốc Y có **TD50 = 800 mg**, **ED50 = 100 mg**. Chọn ĐÚNG:
- A. TI của X = 2; TI của Y = 8
- B. Thuốc Y **an toàn hơn** thuốc X (TI rộng hơn)
- C. TI hẹp nghĩa là khoảng cách liều hiệu quả–độc **nhỏ** → nguy hiểm hơn
- D. Thuốc X an toàn hơn vì ED50 nhỏ hơn TD50
- E. Efficacy của Y chắc chắn cao hơn X vì TI lớn hơn

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C**

- ✅ **A** — X: 300/150=**2**; Y: 800/100=**8**.
- ✅ **B, C** — Y có TI rộng hơn → an toàn hơn.
- ❌ **D** — sai: X có TI hẹp hơn → **kém** an toàn.
- ❌ **E** — sai: TI (an toàn) không nói gì về **efficacy** (tác dụng tối đa). Bẫy trộn khái niệm. *(Ch3)*
</details>

---

### Câu 4 · 🔥 Cực khó
Một biến thể somatic ứng viên: xuất hiện ở **tumor**, **vắng** ở matched normal, nhưng có trong **gnomAD ở AF = 4%**, và bằng chứng ALT gần như **toàn F1R2**. Chọn phát biểu ĐÚNG:
- A. Tần số 4% trong gnomAD gợi ý đây có thể là **biến thể germline phổ biến** → nên bị lọc bởi germline resource
- B. Bằng chứng "toàn F1R2" gợi ý **orientation bias artifact** (đặc biệt nếu mẫu FFPE)
- C. **LearnReadOrientationModel** giúp mô hình hóa và lọc lỗi kiểu này
- D. Vì vắng ở matched normal nên chắc chắn là **driver mutation thật**
- E. **FilterMutectCalls** kết hợp các bằng chứng trên để quyết định giữ/loại

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A** — AF 4% ở quần thể → nghi germline, dùng gnomAD af-only để lọc.
- ✅ **B, C** — toàn F1R2 = orientation bias; LearnReadOrientationModel xử lý.
- ✅ **E** — đúng vai trò FilterMutectCalls.
- ❌ **D** — sai: "vắng ở normal" **không** đủ kết luận driver thật — còn có thể là artifact/germline hiếm bị bỏ sót. Bẫy "chắc chắn". *(Ch4)*
</details>

---

### Câu 5 · 🔴 Rất khó
Về **PRS** và giới hạn:
- A. PRS chỉ dùng thông tin genomics, dựa GWAS (case vs control)
- B. PRS cho **relative risk**, không phải absolute risk
- C. PRS **không** tính yếu tố môi trường/lối sống
- D. Thiên lệch dữ liệu gốc Âu → PRS có thể kém chính xác cho quần thể khác
- E. Hai người cùng PRS chắc chắn phát bệnh cùng thời điểm

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: PRS không cho biết **mốc thời gian** tiến triển. *(Ch5)*
</details>

---

### Câu 6 · 🔴 Rất khó
Về thứ tự & bản chất **pipeline tiền xử lý GATK**:
- A. Map (BWA) → MarkDuplicates → BQSR
- B. MarkDuplicates đánh dấu duplicate do **PCR artifact** + sort tọa độ
- C. BQSR cần **known-sites (dbSNP)**, dùng ML sửa lỗi hệ thống base quality
- D. BQSR có thể chạy trước map để giảm tải
- E. **PU** (Platform Unit) được ưu tiên hơn ID cho recalibration

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E** — D sai: BQSR là bước **cuối** (không thể trước map). *(Ch4)*
</details>

---

### Câu 7 · 🔥 Cực khó
Về cơ chế ung thư ở mức allele (liên hệ oncogene/tumor suppressor):
- A. Oncogene: **gain-of-function**, thường **1 allele** kích hoạt là đủ (trội ở mức tế bào)
- B. Tumor suppressor: **loss-of-function**, thường cần **"two-hit"** (mất cả 2 allele)
- C. Mang **một** biến thể mất chức năng BRCA1 → **tăng nguy cơ**, không gây ung thư ngay
- D. KRAS "luôn bật" là oncogene; TP53/RB1/PTEN là tumor suppressor
- E. Vì somatic không di truyền, mọi driver mutation somatic không thể có yếu tố germline predisposition

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A–D** — đúng (điểm phân biệt 1-hit vs 2-hit).
- ❌ **E** — sai: một số ung thư có **germline predisposition** (vd BRCA di truyền) kết hợp somatic "hit thứ hai". Bẫy "mọi". *(Ch1 + Ch4)*
</details>

---

### Câu 8 · 🔴 Rất khó
Phân biệt **intrinsic** vs **post-hoc** interpretability:
- A. Intrinsic: decision tree, linear/logistic regression, rule-based (RuleFit, RIPPER)
- B. Post-hoc: SHAP, LIME, Grad-CAM (giải thích black-box sau huấn luyện)
- C. SHAP/LIME là intrinsic
- D. Post-hoc thường model-agnostic
- E. Có trade-off accuracy ↔ interpretability

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, D, E** — C sai: SHAP/LIME là **post-hoc**. *(Ch6)*
</details>

---

### Câu 9 · 🔴 Rất khó
Ghép **bậc cấu trúc protein** ↔ liên kết:
- A. Bậc 1 = trình tự aa (liên kết peptit)
- B. Bậc 2 = alpha-helix/beta-sheet (liên kết hidro)
- C. Bậc 3 = gập 3D (cầu di-sulfur, ion)
- D. Bậc 4 = nhiều chuỗi (vd hemoglobin)
- E. Bậc 2 cố định bởi cầu di-sulfur

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: cầu di-sulfur là bậc **3**. *(Ch2)*
</details>

---

### Câu 10 · 🔥 Cực khó
Về **biểu diễn phân tử** và mô hình sinh phân tử (liên hệ generative):
- A. **SELFIES** luôn giải mã thành phân tử hợp lệ → phù hợp sinh phân tử bằng VAE/GAN
- B. **InChI** là định danh chuẩn hóa **duy nhất** (IUPAC)
- C. **Autoencoder (AE)** là lựa chọn tốt nhất để **sinh phân tử mới đa dạng**
- D. **VAE** encoder xuất phân phối (mean+variance) → lấy mẫu → sinh mới; loss = reconstruction + KL
- E. Trong molecular graph, nút = nguyên tử, cạnh = liên kết

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, D, E**

- ✅ **A, B, D, E** — đúng.
- ❌ **C** — sai: AE tái tạo tốt nhưng **khó sinh** mới; VAE/GAN mới dùng để sinh. Bẫy "tốt nhất". *(Ch3)*
</details>

---

### Câu 11 · 🔴 Rất khó
Về **HaplotypeCaller** (4 giai đoạn):
- A. Xác định active regions
- B. Reassembly bằng De Bruijn graph, realign Smith-Waterman
- C. Likelihood bằng PairHMM
- D. Gán genotype bằng Bayes' rule
- E. Loại duplicate bằng PCR ngay trong HaplotypeCaller

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: loại duplicate là của **MarkDuplicates** (tiền xử lý). *(Ch4)*
</details>

---

### Câu 12 · 🔥 Cực khó
Về **GWAS → PRS** và diễn giải kết quả (liên hệ XAI):
- A. Trục Y Manhattan plot = **−log₁₀(P)**; điểm cao = P nhỏ = ý nghĩa mạnh
- B. Biến thể "đạt ngưỡng ý nghĩa" trong GWAS **chắc chắn là nguyên nhân gây bệnh**
- C. Correlation ≠ causation: biến thể liên kết thống kê chưa chắc nhân quả
- D. Không cần biết gene cụ thể vẫn tính được PRS
- E. LD có thể khiến biến thể "tag" đạt ý nghĩa dù không phải biến thể chức năng thật

<details><summary>▸ Đáp án</summary>

**Đúng: A, C, D, E**

- ✅ **A, C, D, E** — đúng (E là điểm khó: LD làm tag-SNP "sáng" trên plot).
- ❌ **B** — sai: liên kết thống kê ≠ nhân quả (nối với correlation≠causation của XAI). Bẫy "chắc chắn". *(Ch5 + Ch6)*
</details>

---

### Câu 13 · 🟠 Khó
Ghép **Drug–Target Interaction** ↔ ví dụ:
- A. 1 thuốc–1 đích: Albuterol → beta2AR (gen ADRB2)
- B. Nhiều thuốc–1 đích: ZMapp (3 kháng thể đơn dòng) trị Ebola
- C. 1 thuốc–nhiều đích: Imatinib (CML, ALL)
- D. Imatinib là ví dụ 1 thuốc–1 đích
- E. ZMapp là small molecule đơn lẻ

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C** — D sai (Imatinib đa đích); E sai (ZMapp là tổ hợp kháng thể). *(Ch1)*
</details>

---

### Câu 14 · 🔴 Rất khó
Về **lọc biến thể germline**:
- A. Hard filter: QD, FS, SOR, MQ, MQRankSum, ReadPosRankSum (vd **QD < 2.0**)
- B. **VQSR** học từ truth set (NA12878...), tính VQSLOD, chạy trên cohort, **riêng SNP/INDEL**
- C. **CNNScoreVariants** (deep learning) tốt cho **single-sample**; CNN_2D dùng cả read data
- D. VQSR nên gộp chung SNP và INDEL trong một mô hình
- E. CNNScoreVariants đặc biệt hợp cho **cohort rất lớn** thay cho VQSR

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C**

- ❌ **D** — VQSR chạy **riêng** SNP/INDEL.
- ❌ **E** — CNNScoreVariants tốt cho **single-sample**; cohort lớn dùng VQSR. *(Ch4)*
</details>

---

### Câu 15 · 🔥 Cực khó
Về **XAI cho GenAI** & đánh giá lời giải thích:
- A. **Hallucination**: đầu ra trôi chảy nhưng sai sự thật → chống bằng **RAG** + Uncertainty Estimation
- B. **Fidelity** đo bằng **PGI**; **Robustness** liên quan spurious correlation → **CD**
- C. **AATS < 0.5** là metric đo **fidelity** của lời giải thích
- D. **Disagreement Problem**: các phương pháp (ABC/BND/PGI) cho kết quả mâu thuẫn
- E. GenAI về bản chất không thể tạo thông tin sai nên không cần verifiability

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, D**

- ❌ **C** — AATS là metric **overfitting của artificial genomes (Ch4)**, không phải fidelity (fidelity = PGI). Bẫy liên chương.
- ❌ **E** — sai: GenAI **có** hallucination → cần verifiability. *(Ch6 + Ch4)*
</details>

---

### Câu 16 · 🔴 Rất khó
Về **DNA / RNA / purine-pyrimidine**:
- A. Purine (2 vòng): A, G; Pyrimidine (1 vòng): C, T, U
- B. RNA dùng ribose (OH ở C2') + Uracil; DNA dùng deoxyribose + Thymine
- C. Nhóm phốt phát gắn C5', bazơ gắn C1'
- D. Bắt cặp: A–T, G–C (mỗi cặp = 1 purine + 1 pyrimidine)
- E. Uracil là purine

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: U là **pyrimidine**. *(Ch2)*
</details>

---

### Câu 17 · 🔴 Rất khó
Về **PK/PD/ADME**:
- A. PK = "cơ thể làm gì với thuốc" (ADME); PD = "thuốc làm gì với cơ thể"
- B. Chuyển hóa chủ yếu ở gan (Pha I: cytochrome P450); thải trừ chủ yếu ở thận
- C. Pha II (liên hợp) làm thuốc tan trong nước hơn
- D. Agonist chặn receptor; antagonist kích hoạt receptor
- E. Half-life = thời gian nồng độ giảm 50%

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E** — D sai: đảo ngược (agonist kích hoạt, antagonist chặn). *(Ch3)*
</details>

---

### Câu 18 · 🔴 Rất khó
Về **hai bài toán ML ung thư** (personalized medicine):
- A. Cancer Subtyping → chẩn đoán/phân nhóm bệnh nhân
- B. Drug Response Prediction → điều trị
- C. Cả hai dùng: CNV, mutation, methylation, gene expression, clinical data
- D. NCI-DREAM có sub-challenge Drug Sensitivity & Drug Synergy
- E. Hai bài toán dùng hai bộ đặc trưng hoàn toàn khác nhau

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: dùng **cùng** bộ đặc trưng, khác mục tiêu. *(Ch5)*
</details>

---

### Câu 19 · 🔥 Cực khó
So sánh **EVE** vs **AlphaMissense** (dự đoán biến thể gây bệnh):
- A. EVE = **Bayesian VAE**, học từ **MSA**, **KHÔNG cần nhãn** (unsupervised)
- B. EVE tính evolutionary index → **GMM** phân benign/pathogenic
- C. AlphaMissense = fine-tune **AlphaFold** (transformer, không phải VAE) + structural context
- D. Bayesian VAE cho **uncertainty** (weights là phân phối), train bằng **ELBO**
- E. Cả EVE lẫn AlphaMissense đều là discriminative huấn luyện trực tiếp trên nhãn ClinVar

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: EVE **unsupervised** (ClinVar chỉ dùng để **đánh giá**). *(Ch4)*
</details>

---

### Câu 20 · 🔴 Rất khó
Về **phương pháp diễn giải post-hoc**:
- A. SHAP dựa giá trị Shapley (game theory), giải thích cả cục bộ & toàn cục
- B. LIME giải thích **cục bộ** (Local), model-agnostic
- C. Grad-CAM/Grad-CAM++ tạo heatmap cho ảnh (CNN)
- D. Counterfactual: "nếu input khác đi thì sao"
- E. LIME giải thích ở mức toàn cục cho cả mô hình

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: LIME = **Local** (cục bộ). *(Ch6)*
</details>

---

### Câu 21 · 🔥 Cực khó
Về **GVCF workflow** & N+1 problem — chọn ĐÚNG:
- A. Mỗi mẫu chạy HaplotypeCaller `-ERC GVCF`; gộp bằng **GenomicsDBImport**; joint bằng **GenotypeGVCFs**
- B. Giải quyết **N+1 problem**: thêm mẫu mới chỉ cần cập nhật DB, không chạy lại toàn bộ
- C. **GenotypeGVCFs** xuất **mọi** vị trí (kể cả không biến thể ở tất cả mẫu)
- D. GATK4 dùng GenomicsDBImport; GATK3 dùng CombineGVCFs
- E. GVCF thô của **một mẫu** có record cho mọi vị trí (kể cả non-variant blocks)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, D, E**

- ✅ **E** — đúng, đây là điểm tinh tế: **GVCF một mẫu** có non-variant blocks...
- ❌ **C** — nhưng **GenotypeGVCFs** (sau joint) chỉ xuất **site biến thể ở ≥1 mẫu**. Phân biệt C (sai) vs E (đúng). *(Ch4)*
</details>

---

### Câu 22 · 🟠 Khó
Về **drug repositioning** & khung Disease–Gene–Drug:
- A. ~75% thuốc *lý thuyết* có thể tái định vị; ~30% thuốc duyệt/năm là repositioned
- B. Drug–Disease association chính là bài toán repositioning
- C. Network-based dựa **disease module principle**
- D. Do thiếu nhãn âm, ML hay dùng **PU learning**
- E. Repositioning bắt buộc phát triển phân tử mới từ đầu

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: bản chất là **dùng lại** thuốc đã có. *(Ch1)*
</details>

---

### Câu 23 · 🔴 Rất khó
Về **Micro vs Macro view** (identify key factors):
- A. Micro: knowledge neuron, receptive fields
- B. **Polysemanticity**: 1 neuron mã hóa **nhiều** khái niệm → hạn chế micro
- C. Macro: distributed representations
- D. Mechanistic interpretability = "virtual neuroscience"
- E. Polysemanticity = 1 neuron chỉ mã hóa 1 khái niệm

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: polysemanticity = **nhiều** khái niệm/neuron. *(Ch6)*
</details>

---

### Câu 24 · 🔥 Cực khó
Về **Somatic CNV** (copy ratio & segmentation):
- A. Pipeline: PreprocessIntervals → CollectReadCounts → CreateReadCountPanelOfNormals → **DenoiseReadCounts** → **ModelSegments** → **CallCopyRatioSegments**
- B. DenoiseReadCounts: chuẩn hóa theo median PoN (log2) → denoise bằng **PCA** của PoN
- C. **Minor Allele Fraction** (site het) lộ **allelic imbalance** mà copy-ratio không thấy
- D. penalty **λ thấp** → segmentation nhạy hơn (nhiều breakpoint); λ cao → robust hơn
- E. PoN cho CNV **giống hệt** PoN cho somatic short variant

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: PoN CNV **khác hoàn toàn** (cần ≥10, khuyến nghị ≥40 normal). *(Ch4)*
</details>

---

### Câu 25 · 🔥 Cực khó
Một đột biến thêm **2 nucleotide** vào giữa vùng mã hóa. Chọn phát biểu ĐÚNG:
- A. Đây là **frameshift** (thêm/mất không phải bội số 3) → lệch khung đọc
- B. Có thể tạo **stop codon sớm** ở downstream do khung đọc bị lệch
- C. Nếu thêm đúng **3** nucleotide thì **không** gây frameshift (in-frame insertion)
- D. **Nonsense** = đổi 1 axit amin; **Missense** = tạo stop codon sớm
- E. Công cụ như **Funcotator/VEP** có thể annotate loại hậu quả này

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E**

- ✅ **A, B, C, E** — đúng (2 nt → frameshift; 3 nt → in-frame).
- ❌ **D** — sai: **đảo ngược** — nonsense = tạo stop sớm; missense = đổi aa. *(Ch2 + Ch4)*
</details>

---

### Câu 26 · 🟠 Khó
Ghép **4 loại thuốc**:
- A. Small molecule <900 Da, thường uống (Aspirin, Metformin, Statin)
- B. Biologics (Herceptin, insulin, vắc-xin), thường tiêm
- C. LBA chứa sinh vật sống (Lactobacillus, FMT)
- D. Cell therapy: CAR-T (Kymriah, Yescarta)
- E. Herceptin là small molecule vì nhắm đích đặc hiệu

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: Herceptin là **biologics** (kháng thể). *(Ch3)*
</details>

---

### Câu 27 · 🔴 Rất khó
Ghép **-omics** ↔ đối tượng:
- A. Genomics=DNA; Transcriptomics=RNA (snapshot biểu hiện gen)
- B. Proteomics=protein (functional output); Metabolomics=phân tử nhỏ
- C. Central Dogma: DNA→RNA→Protein→Metabolite
- D. PGx dựa đa -omics; Personalized Medicine chỉ dựa genomics
- E. Transcriptomics = metabolite

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C**

- ❌ **D** — đảo ngược: **PGx = chỉ genomics**, Personalized = đa -omics.
- ❌ **E** — transcriptomics = **RNA**. *(Ch5)*
</details>

---

### Câu 28 · 🔴 Rất khó
Về **Mutect2** & tài nguyên somatic:
- A. Paradigm Tumor–Normal pair
- B. **PoN** loại artifact kỹ thuật & germline phổ biến mức quần thể
- C. **Matched normal** loại germline đặc thù cá nhân
- D. **Germline resource** (gnomAD af-only) lọc germline theo tần số
- E. Không thể chạy nếu thiếu matched normal

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: có chế độ **tumor-only**. *(Ch4)*
</details>

---

### Câu 29 · 🔴 Rất khó
Về **5 chiều đánh giá** lời giải thích:
- A. Fidelity (đo bằng PGI)
- B. Interpretability
- C. Robustness (spurious correlation → CD)
- D. Fairness & Completeness/Ablation
- E. Fidelity đo bằng AATS

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: Fidelity = **PGI** (AATS thuộc Ch4). *(Ch6)*
</details>

---

### Câu 30 · 🔥 Cực khó
Về **strand bias** vs **orientation bias**:
- A. Strand: forward vs reverse; Orientation (F/R): hướng read map vào reference
- B. Strand bias: ALT chỉ từ 1 strand (toàn forward/reverse)
- C. Orientation bias: lỗi hóa học library prep (vd G→T), quan trọng với **FFPE**; ALT gần như toàn F1R2 hoặc toàn F2R1
- D. F1R2 = read1+read2 từ sợi forward; F2R1 = từ sợi reverse
- E. Hai hiện tượng này là một, chỉ khác tên gọi

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: **hai hiện tượng khác nhau**. *(Ch4)*
</details>

---

### Câu 31 · 🟠 Khó
Về **NIPT** (sàng lọc trước sinh):
- A. Dựa cfDNA của thai trong máu mẹ, giải trình tự phát hiện lệch bội
- B. Là xét nghiệm **không xâm lấn**
- C. Phát hiện Trisomy 21, 18, 13
- D. Là xét nghiệm chẩn đoán xác định, dương tính không cần khẳng định
- E. Dương tính vẫn cần xét nghiệm xâm lấn (chọc ối) khẳng định

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E** — D sai: NIPT là **sàng lọc**, không phải chẩn đoán. *(Ch1)*
</details>

---

### Câu 32 · 🔴 Rất khó
Về **Disagreement Problem** & thách thức XAI tin sinh:
- A. Các phương pháp giải thích cho kết quả **mâu thuẫn** về cùng dự đoán
- B. Correlation ≠ Causation: feature "quan trọng" chưa chắc nhân quả
- C. Giải pháp: causal inference, ProtoPNet, Concept Bottleneck Models
- D. Feature quan trọng theo SHAP **luôn** là nguyên nhân gây bệnh
- E. Biological noise vs signal là một thách thức thực

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E** — D sai: correlation ≠ causation. *(Ch6)*
</details>

---

### Câu 33 · 🔴 Rất khó
Ghép **định dạng dữ liệu**:
- A. FASTA = reference (không cần quality score)
- B. FASTQ = trình tự + Phred quality
- C. BAM = SAM nén BGZF (~1/5)
- D. GVCF = record cho mọi vị trí (multi-sample)
- E. Reference nên lưu FASTQ vì cần quality score

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: reference dùng **FASTA**. *(Ch4)*
</details>

---

### Câu 34 · 🔴 Rất khó
Về **phiên mã** ở nhân thực:
- A. Intron bị loại, exon giữ lại (RNA splicing loại intron)
- B. Intron thường theo quy tắc GT–AG
- C. Nắp 5' + đuôi poly-A: vận chuyển ra tế bào chất, chống thủy phân, giúp ribosome gắn
- D. Alternative splicing → 1 gene tạo nhiều protein
- E. Splicing loại bỏ exon, giữ intron

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: splicing loại **intron**. *(Ch2)*
</details>

---

### Câu 35 · 🔴 Rất khó
Về **GNN** & message passing:
- A. Mỗi nút tổng hợp thông tin từ nút lân cận qua cạnh; lặp lớp → mở rộng receptive field
- B. GNN cần permutation invariant
- C. Node classification / link prediction / graph-level là 3 output
- D. DTI = **link prediction**; độc tính cả phân tử = **graph-level** (pooling)
- E. GNN chỉ hoạt động trên lưới đều như CNN

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: GNN xử lý **đồ thị phi-Euclid**. *(Ch3)*
</details>

---

### Câu 36 · 🟠 Khó
Về **absolute risk** vs **relative risk**:
- A. Absolute risk = khả năng bệnh xảy ra thực sự (vd BRCA1 → 60–80% ung thư vú)
- B. Relative risk so với nhóm tham chiếu
- C. PRS cho relative risk, không phải absolute
- D. Nguy cơ tuyệt đối trọn đời phụ thuộc tuổi/thời gian quan sát
- E. Hai khái niệm là như nhau

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: **khác nhau**. *(Ch5)*
</details>

---

### Câu 37 · 🔥 Cực khó
So sánh mô hình sinh (xuyên Ch3–Ch4) — chọn ĐÚNG:
- A. **GAN** dùng Jensen-Shannon divergence; **WGAN** dùng **Wasserstein** + **Critic**
- B. **RBM** có 2 lớp visible–hidden; **CNN** tốt cho motif/LD (cấu trúc cục bộ)
- C. **VAE** đa dạng nhưng "blurry"; **GAN** sắc nét (high-fidelity) nhưng dễ **mode collapse**
- D. **AATS < 0.5** chỉ ra artificial genomes bị **overfit**
- E. WGAN dùng Jensen-Shannon; GAN dùng Wasserstein

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: đảo ngược GAN↔WGAN. *(Ch3 + Ch4)*
</details>

---

### Câu 38 · 🔴 Rất khó
Ứng dụng & bài toán hiện đại XAI (healthcare):
- A. Grad-CAM++ phát hiện khối u não từ ảnh
- B. Diễn giải trên EMR (electronic medical records)
- C. Mirror Effect: so saliency của AI với fMRI não người
- D. Case study: Random Forest + SHAP dự đoán subtype ung thư vú
- E. AlphaFold diễn giải attention nội bộ trong dự đoán cấu trúc protein

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E** — tất cả đúng (cảnh giác: multiple-select đôi khi toàn đúng). *(Ch6)*
</details>

---

### Câu 39 · 🔴 Rất khó
Về **biến thể di truyền** & zygosity:
- A. SNV/SNP nhỏ (<50 bp); CNV/inversion/translocation là structural variant (lớn)
- B. Heterozygous = biến thể ở **1** NST; Homozygous = ở **cả 2**
- C. Hai người khác nhau ~1 SNV mỗi 1000 bp (~2,7 triệu khác biệt, ~0,1%)
- D. Indel > 50 bp được xếp vào structural variant
- E. Heterozygous = biến thể ở cả 2 NST

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: het = **1** NST (E mô tả homozygous). *(Ch4)*
</details>

---

### Câu 40 · 🟠 Khó
Về khung **Disease–Gene–Drug** & cách tiếp cận:
- A. 3 liên kết: Drug–Target, Disease–Gene, Drug–Disease
- B. Disease module principle → nền network-based
- C. ML hay dùng PU learning / bán giám sát (thiếu nhãn âm)
- D. 3 cách tiếp cận: network-based, ML-based, data-mining-based
- E. Data-mining-based không thuộc các cách tiếp cận được nêu

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: data-mining **CÓ** thuộc. *(Ch1)*
</details>

---

### Câu 41 · 🔴 Rất khó
Về **XAI cho GenAI**:
- A. Infinite output variability là thách thức riêng
- B. Hallucination: trôi chảy nhưng non-factual
- C. RAG hỗ trợ verifiability (kiểm chứng nội dung sinh)
- D. Explanation as dialogue: từ heatmap tĩnh → hội thoại lặp
- E. GenAI không bao giờ tạo thông tin sai

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: GenAI **có** hallucination. *(Ch6)*
</details>

---

### Câu 42 · 🔴 Rất khó
Về **codon / tRNA / mã di truyền**:
- A. 1 start codon (ATG=Met); 3 stop codon (TAA/TAG/TGA)
- B. 61 tRNA, mỗi cái mang một anticodon
- C. Có 64 codon; mã di truyền **thoái hóa** (nhiều codon → 1 aa)
- D. ORF: bội số 3, bắt đầu start, kết thúc stop, giữa không có stop
- E. Vì có 20 aa nên chỉ có đúng 20 codon

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: có **64** codon. *(Ch2)*
</details>

---

### Câu 43 · 🔴 Rất khó
Về **Morgan fingerprint / QSAR / descriptor**:
- A. Morgan (ECFP): cấu trúc con hình tròn theo radius, băm thành vector nhị phân (có hash collision)
- B. QSAR: Structure → Descriptor → Activity/Toxicity
- C. logP cao → dễ qua màng, khó tan nước; HBD = số nhóm cho liên kết hidro
- D. Hỗ trợ trong RDKit; dùng cho similarity search / virtual screening
- E. Morgan fingerprint chỉ dùng cho protein

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: dùng cho phân tử thuốc nhỏ/hợp chất. *(Ch3)*
</details>

---

### Câu 44 · 🟠 Khó
Về sinh dữ liệu -omics & tài nguyên:
- A. Omics là big data → cần AI; thách thức: translational research (bench→bedside)
- B. DMET chip: 1936 SNP / 231 gene (PGx)
- C. gnomAD (tiền thân ExAC); COSMIC (soma); TCGA/GDC
- D. WGS ~3,1 tỷ bp; WES ~1,4% WGS
- E. Omics data nhỏ, xử lý bằng tay được

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: là **big data**. *(Ch5)*
</details>

---

### Câu 45 · 🔴 Rất khó
Về **đánh giá callset** (Ti/Tv):
- A. Ti/Tv = transition/transversion
- B. Transition (A↔G, C↔T) phổ biến hơn transversion
- C. Ti/Tv lệch bất thường → dấu hiệu chất lượng kém
- D. GATK VariantEval so với dbSNP / truth set
- E. Transversion phổ biến hơn transition

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai: **transition** phổ biến hơn. *(Ch4)*
</details>

---

### Câu 46 · 🔥 Cực khó
**Chọn TẤT CẢ phát biểu SAI:**
- A. PGx tích hợp toàn bộ đa -omics của cá nhân
- B. Trục Y Manhattan plot là P-value (không log)
- C. PRS cho absolute risk chính xác cho mọi chủng tộc
- D. Cancer subtyping phục vụ điều trị; drug response phục vụ chẩn đoán
- E. Proteomics là toàn bộ RNA của tế bào

<details><summary>▸ Đáp án</summary>

**SAI: A, B, C, D, E (cả 5)**

- ❌ A: đó là **Personalized Medicine** (PGx = chỉ genomics).
- ❌ B: trục Y là **−log(P)**.
- ❌ C: PRS = relative, thiên lệch gốc Âu, là xác suất.
- ❌ D: đảo ngược (subtyping→chẩn đoán, drug response→điều trị).
- ❌ E: proteomics = **protein**. *(Ch5)*
</details>

---

### Câu 47 · 🔴 Rất khó
**Chọn TẤT CẢ phát biểu SAI** (mix Ch1–Ch3):
- A. Discriminative học P(X) để sinh dữ liệu mới
- B. Oncogene cần "two-hit" mới gây bệnh
- C. TI hẹp = thuốc an toàn hơn
- D. AE là generative model mạnh để sinh phân tử đa dạng
- E. Antagonist kích hoạt receptor tạo đáp ứng

<details><summary>▸ Đáp án</summary>

**SAI: A, B, C, D, E (cả 5)**

- ❌ A: đảo discriminative/generative.
- ❌ B: two-hit là của **tumor suppressor**.
- ❌ C: TI hẹp = **nguy hiểm hơn**.
- ❌ D: AE **khó sinh** mới.
- ❌ E: antagonist **chặn** receptor. *(Ch1+Ch3)*
</details>

---

### Câu 48 · 🔥 Cực khó
Về **GNN output** ghép ví dụ (chọn ĐÚNG):
- A. **Node classification** → phân loại user spam/không spam
- B. **Link prediction** → dự đoán **drug–target interaction**, gợi ý kết bạn
- C. **Graph-level** (pooling: sum/mean/max/attention) → dự đoán độc tính/độ tan **cả phân tử**
- D. **DTI** nên giải bằng **graph-level pooling** thay vì link prediction
- E. Geometric deep learning mở rộng DL sang miền phi-Euclid (đồ thị, manifold)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, E** — D sai: DTI = **link prediction** (dự đoán cạnh), không phải graph-level. *(Ch3)*
</details>

---

### Câu 49 · 🔴 Rất khó
Về **công nghệ giải trình tự** & WGS/WES:
- A. Illumina: short read (50–150 bp), lỗi thấp, phổ biến
- B. PacBio & Nanopore: long read, lỗi cao hơn Illumina
- C. Paired-end giúp xử lý vùng lặp & gợi ý structural variant
- D. WES ~1,4% genome, coverage sâu hơn ở vùng mã hóa nhưng bỏ non-coding
- E. Illumina lỗi cao hơn PacBio; Chromium 10x đắt hơn PacBio

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D** — E sai (kép): Illumina lỗi **thấp** hơn; Chromium 10x **rẻ** hơn PacBio. *(Ch4)*
</details>

---

### Câu 50 · 🔥 Cực khó
**Tổng hợp bẫy — chọn TẤT CẢ phát biểu SAI** (mix Ch4 + Ch6):
- A. BQSR chạy trước MarkDuplicates để tối ưu
- B. VQSR chạy chung SNP và INDEL trong một mô hình
- C. EVE là mô hình discriminative huấn luyện trên nhãn ClinVar
- D. LIME giải thích ở mức toàn cục; SHAP là intrinsic
- E. GenotypeGVCFs xuất mọi vị trí kể cả non-variant

<details><summary>▸ Đáp án</summary>

**SAI: A, B, C, D, E (cả 5)**

- ❌ A: BQSR là bước **cuối** tiền xử lý.
- ❌ B: VQSR chạy **riêng** SNP/INDEL.
- ❌ C: EVE **unsupervised** (ClinVar chỉ để đánh giá).
- ❌ D: LIME = **cục bộ**; SHAP = **post-hoc**.
- ❌ E: GenotypeGVCFs chỉ xuất site **biến thể**. *(Ch4 + Ch6)*

> 🎯 5 câu SAI này gom đúng **5 bẫy hay gặp nhất** của môn — nếu nhận ra hết, bạn đã nắm chắc phần lõi.
</details>

---

## 📊 Bảng tra nhanh (sau khi làm xong)

| Chủ đề gặp nhiều | Câu số |
|---|---|
| Ch1 – GenAI/Disease-Gene-Drug | 1, 7, 13, 22, 31, 40, 47 |
| Ch2 – Sinh học phân tử | 2, 9, 16, 25, 34, 42 |
| Ch3 – Khám phá thuốc | 3, 10, 17, 26, 35, 37, 43, 48 |
| Ch4 – GATK ⭐ | 4, 6, 11, 14, 19, 21, 24, 28, 30, 33, 39, 45, 49, 50 |
| Ch5 – Y học cá thể hóa | 5, 12, 18, 27, 36, 44, 46 |
| Ch6 – XAI | 8, 15, 20, 23, 29, 32, 38, 41, 50 |

**Cách chấm:** mỗi câu chỉ tính đúng khi bạn chọn **chính xác toàn bộ** phương án đúng (không thừa, không thiếu) — đúng chuẩn multiple-select. Dưới 35/50 → nên đọc lại các mục 🔴 trong `../on_tap/`.
