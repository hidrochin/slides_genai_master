# Trắc nghiệm Chương 6 – Trí tuệ nhân tạo diễn giải (Explainable AI – XAI)

> ⚠️ **Multiple-select: mỗi câu có 0→nhiều đáp án đúng.** Xét **từng phương án như một câu Đúng/Sai độc lập**.
> 🎚️ Độ khó: 🟢 TB · 🟠 Khó · 🔴 Rất khó. Giải thích trong khối **▸ Đáp án** dưới mỗi câu — tự làm trước khi mở.

---

### Câu 1 · 🟠 Khó
Vì sao cần **XAI** trong tin sinh/y tế:
- A. Quyết định **rủi ro cao** (chẩn đoán, khám phá thuốc)
- B. Lý do **pháp lý/quy định** (FDA, GDPR)
- C. Niềm tin & sự chấp nhận của bác sĩ/nhà sinh học
- D. Vấn đề "black box": **hiệu năng tăng → khả năng diễn giải giảm**
- E. Mục tiêu chính của XAI là **tăng accuracy lên 100%**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: XAI **không** nhằm tăng accuracy; thậm chí có **trade-off** accuracy↔interpretability.
</details>

---

### Câu 2 · 🔴 Rất khó
Phân biệt **intrinsic** vs **post-hoc** interpretability:
- A. **Intrinsic** = mô hình tự dễ diễn giải (decision tree, linear/logistic regression, rule-based)
- B. **Post-hoc** = giải thích black-box **sau** huấn luyện (SHAP, LIME, Grad-CAM)
- C. SHAP và LIME là ví dụ của **intrinsic**
- D. Có **trade-off** giữa accuracy và interpretability
- E. Post-hoc thường **model-agnostic** (không phụ thuộc kiến trúc mô hình)
- F. RuleFit, RIPPER là mô hình **intrinsic**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, D, E, F**

- ✅ **A, B, D, E, F** — đúng.
- ❌ **C** — sai: SHAP/LIME là **post-hoc**, không phải intrinsic. Bẫy kinh điển.
</details>

---

### Câu 3 · 🔴 Rất khó
Về **5 chiều đánh giá** một lời giải thích:
- A. **Fidelity** (trung thực) — phản ánh chính xác hành vi mô hình gốc; đo bằng **PGI**
- B. **Interpretability** — con người có hiểu được không
- C. **Robustness** — ổn định khi input bị nhiễu nhẹ; liên quan **spurious correlation** → **CD (Correlation Difference)**
- D. **Fairness** & **Completeness/Ablation**
- E. Fidelity được đo bằng **AATS** (Adversarial Accuracy)
- F. Nếu lời giải thích "vỡ" dưới nhiễu → robustness kém → **không tin cậy**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng (đủ 5 chiều + PGI + CD).
- ❌ **E** — sai: Fidelity đo bằng **PGI**; **AATS** là metric overfitting của artificial genomes (Ch4) — gài liên chương.
</details>

---

### Câu 4 · 🟠 Khó
Về **The Disagreement Problem**:
- A. Các phương pháp giải thích khác nhau cho kết quả **mâu thuẫn** về cùng một dự đoán
- B. ABC, BND, PGI là các phương pháp/metric liên quan
- C. Là hiện tượng các phương pháp **luôn đồng ý** với nhau
- D. Chỉ xảy ra với mô hình **intrinsic**
- E. Làm giảm niềm tin vào lời giải thích khi chúng không nhất quán

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, E**

- ✅ **A, B, E** — đúng.
- ❌ **C** — sai: là hiện tượng **mâu thuẫn**, không đồng ý.
- ❌ **D** — sai: không giới hạn ở intrinsic (chủ yếu ở post-hoc trên black-box).
</details>

---

### Câu 5 · 🔴 Rất khó
Thách thức riêng khi diễn giải **GenAI**:
- A. **Infinite output variability** (đầu ra biến thiên vô hạn)
- B. **Hallucination**: đầu ra trôi chảy nhưng **sai sự thật (non-factual)**
- C. Cần **prompt engineering control**
- D. Chống hallucination bằng **Uncertainty Estimation** & **RAG**
- E. GenAI **không bao giờ** tạo ra thông tin sai
- F. **RAG** hỗ trợ **verifiability** (kiểm chứng nội dung sinh ra)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: GenAI **có** tạo hallucination (đó chính là vấn đề cần giải). Bẫy "tuyệt đối".
</details>

---

### Câu 6 · 🔴 Rất khó
Ghép **phương pháp diễn giải post-hoc** ↔ đặc điểm:
- A. **SHAP** — dựa **giá trị Shapley** (lý thuyết trò chơi); giải thích cả **cục bộ & toàn cục**
- B. **LIME** — giải thích **cục bộ (local)**, model-agnostic
- C. **Grad-CAM / Grad-CAM++** — **heatmap** cho ảnh (CNN)
- D. **Counterfactual explanation** — "nếu input khác đi thì sao"
- E. **LIME** giải thích ở mức **toàn cục** cho toàn bộ mô hình
- F. **Permutation importance** đo tầm quan trọng feature bằng xáo trộn

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: LIME = **Local** Interpretable Model-agnostic Explanations → **cục bộ**, không toàn cục. Bẫy chữ "Local" trong tên.
</details>

---

### Câu 7 · 🔴 Rất khó
Về **Micro View** vs **Macro View**:
- A. **Micro**: knowledge neuron, receptive fields, feature visualization
- B. **Polysemanticity**: một neuron mã hóa **nhiều** khái niệm → hạn chế của micro view
- C. **Macro**: distributed representations (biểu diễn phân tán trên nhiều neuron)
- D. **Mechanistic interpretability** = "virtual neuroscience"
- E. Polysemanticity nghĩa là một neuron chỉ mã hóa **một** khái niệm duy nhất
- F. **Psychophysics for Machines** thuộc góc nhìn hành vi (behavioural / artificial cognition)

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, F**

- ✅ **A, B, C, D, F** — đúng.
- ❌ **E** — sai: polysemanticity = một neuron mã hóa **nhiều** khái niệm (chính vì thế khó diễn giải). Bẫy đảo nghĩa.
</details>

---

### Câu 8 · 🟠 Khó
Ứng dụng **XAI trong tin sinh** (bài coding):
- A. Gene expression analysis (diễn giải gene quan trọng trong phân loại ung thư)
- B. Single-cell RNA-seq (xác định marker chính)
- C. Biomarker discovery (feature selection + interpretation)
- D. **AlphaFold** diễn giải **attention** nội bộ trong dự đoán cấu trúc protein
- E. Drug response prediction

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E** (tất cả đều đúng)

- ✅ Cả 5 đều là ứng dụng hợp lệ được nêu — cảnh giác vì multiple-select có thể tất cả đúng.
</details>

---

### Câu 9 · 🔴 Rất khó
Thách thức XAI trong tin sinh:
- A. **Biological noise vs signal** (nhiễu sinh học)
- B. **Correlation ≠ Causation**: feature "quan trọng" **chưa chắc** nhân quả
- C. Data bias & model artifacts
- D. Giải pháp mới nổi: **causal inference**, interpretable deep models (**ProtoPNet, Concept Bottleneck Models**), Responsible AI
- E. Feature quan trọng theo SHAP **luôn** là nguyên nhân gây bệnh

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D**

- ✅ **A, B, C, D** — đúng.
- ❌ **E** — sai: correlation ≠ causation → feature quan trọng **chưa chắc** là nguyên nhân. (Liên hệ giới hạn PRS ở Ch5.)
</details>

---

### Câu 10 · 🟠 Khó
Diễn giải trong bài toán hiện đại (healthcare):
- A. **Grad-CAM++** phát hiện **khối u não** từ ảnh
- B. Diễn giải trên **EMR (Electronic Medical Records)** — "beyond the pixel"
- C. **Mirror Effect**: so **saliency map** của AI với ảnh **fMRI** não người
- D. Case study: **Random Forest + SHAP** dự đoán subtype ung thư vú từ gene expression
- E. **ProtoPNet** và **Concept Bottleneck Models** là mô hình **interpretable-by-design**

<details><summary>▸ Đáp án</summary>

**Đúng: A, B, C, D, E** (tất cả đúng)

- ✅ Cả 5 đúng — đều là nội dung mục 6.6 & bài coding.
</details>

---

### Câu 11 · 🔴 Rất khó
Chọn **TẤT CẢ** phát biểu **SAI**:
- A. SHAP và LIME là phương pháp intrinsic
- B. LIME giải thích ở mức toàn cục
- C. Hiệu năng mô hình càng cao thì càng dễ diễn giải
- D. Polysemanticity nghĩa là một neuron chỉ mã hóa một khái niệm
- E. Fidelity được đo bằng metric AATS

<details><summary>▸ Đáp án</summary>

**SAI: A, B, C, D, E** (cả 5 đều sai)

- ❌ **A** — SHAP/LIME là **post-hoc**.
- ❌ **B** — LIME = **cục bộ**.
- ❌ **C** — ngược lại: hiệu năng cao → thường **khó** diễn giải (trade-off).
- ❌ **D** — polysemanticity = **nhiều** khái niệm/neuron.
- ❌ **E** — Fidelity đo bằng **PGI** (AATS là của Ch4).
</details>
