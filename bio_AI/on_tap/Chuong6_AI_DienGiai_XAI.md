# Chương 6 – Trí tuệ nhân tạo diễn giải (Explainable AI – XAI)

> Slide chương này nặng hình ảnh, ít chữ → file này bổ sung kiến thức nền để hiểu trọn vẹn. Cấu trúc gồm 6 mục + bài thực hành coding.

**Nội dung (6 mục):**
- 6.1. Giới thiệu XAI
- 6.2. XAI trong GenAI
- 6.3. Một số phương pháp diễn giải áp dụng cho GenAI
- 6.4. Đánh giá diễn giải bằng dữ liệu thực nghiệm
- 6.5. Xác định yếu tố sinh học chính trong mô hình AI
- 6.6. Diễn giải trong các bài toán hiện đại

---

## 6.1. Giới thiệu XAI ⭐
- **Vấn đề "black box"**: mô hình deep learning là "hộp đen" – **hiệu năng tăng thì khả năng diễn giải giảm** → khủng hoảng niềm tin ở lĩnh vực rủi ro cao (y tế, tài chính).
- **Vì sao cần diễn giải trong tin sinh?**
  - Quyết định rủi ro cao: chẩn đoán, khám phá thuốc.
  - Lý do pháp lý/quy định: **FDA, GDPR** compliance.
  - Niềm tin & sự chấp nhận của bác sĩ/nhà sinh học.

### Hai loại diễn giải ⭐
| Loại | Mô tả | Ví dụ |
|---|---|---|
| **Intrinsic (nội tại)** | Bản thân mô hình đã dễ diễn giải | Decision tree, linear/logistic regression, rule-based (RuleFit, RIPPER) |
| **Post-hoc (hậu kỳ)** | Giải thích mô hình black-box **sau khi** huấn luyện | **SHAP, LIME**, Grad-CAM, permutation importance |

- **Trade-off Accuracy ↔ Interpretability**: mô hình càng chính xác thường càng khó diễn giải.

### 5 chiều đánh giá một lời giải thích (Evaluation Dimensions) ⭐
1. **Fidelity (trung thực)** – "tấm gương của sự thật": lời giải thích phản ánh **chính xác** hành vi mô hình gốc đến đâu. Đo bằng **PGI (Prediction Gap on Importance)**.
2. **Interpretability (khả hiểu)**: con người có hiểu được không? (giao diện người dùng).
3. **Robustness (bền vững)**: lời giải thích có ổn định khi input bị nhiễu nhẹ (perturbation) không? Vỡ dưới nhiễu → không tin cậy. Liên quan **spurious correlation** (tương quan giả) → giải bằng **Correlation Difference (CD)**.
4. **Fairness (công bằng)**.
5. **Completeness (đầy đủ)** & **Ablation**.

- **The Disagreement Problem** ⭐: các phương pháp giải thích khác nhau (vd **ABC** – Attribution-Based Confidence, **BND** – Baseline-Noise Difference, **PGI**) cho kết quả **mâu thuẫn nhau** về cùng một dự đoán.
- **From Engineer to Artificial Cognition**: "Psychophysics for Machines" – coi AI như **đối tượng thí nghiệm tâm lý học**, đo hành vi (response time) thay vì trọng số.

---

## 6.2. XAI trong GenAI (Explainable Generative AI) ⭐
- **Từ Quyết định đến Sáng tạo (From Decision to Creation)**: XAI truyền thống giải thích **phân loại**; GenAI cần giải thích **sinh dữ liệu**.
- **Thách thức riêng của GenAI:**
  - **Infinite output variability** (đầu ra biến thiên vô hạn).
  - **Hallucination** (ảo giác): đầu ra trôi chảy nhưng **sai sự thật (non-factual)**.
  - Cần **prompt engineering control**.
- **Chống hallucination bằng Verifiability**: XAI hỗ trợ kiểm chứng nội dung sinh ra qua **Uncertainty Estimation** và **RAG (Retrieval-Augmented Generation)**.
- **Explanation as Dialogue**: chuyển từ heatmap tĩnh → tinh chỉnh hội thoại lặp.
- **Decoding in Latent Spaces**: giải thích cách không gian ẩn (hidden space) trở thành cấu trúc qua **concept attribution**.
- **Mechanistic Interpretability**: "khoa học thần kinh ảo" (virtual neuroscience) – phân tích cơ chế nội tại của mô hình.

---

## 6.3. Các phương pháp diễn giải cho GenAI ⭐
- **Chain-of-Thought (CoT)** & vấn đề **unfaithful self-explanation** (mô hình tự giải thích không trung thực).
- **Probe internal state** (thăm dò trạng thái nội bộ).
- **Feature Attributions in Text** (gán tầm quan trọng cho token).
- **Visualization / Feature Visualization**.
- **Disentanglement** (tách biệt yếu tố sinh trong latent).
- **Inside the diffusion process** (giải thích quá trình khuếch tán).
- **Counterfactual explanation** (giải thích phản thực: "nếu input khác đi thì sao").
- **Concept Attribution** (gán khái niệm).
- **RAG as XAI** (RAG như một cơ chế giải thích – truy xuất bằng chứng).

**Các phương pháp post-hoc kinh điển (từ bài coding):**
- **Feature importance**: permutation importance.
- **LIME** (Local Interpretable Model-agnostic Explanations) – giải thích **cục bộ**.
- **SHAP** (SHapley Additive exPlanations) – dựa trên **giá trị Shapley** (lý thuyết trò chơi), giải thích cả cục bộ & toàn cục.
- **Grad-CAM / Grad-CAM++** ("con mắt số") – bản đồ nhiệt cho ảnh (CNN).
- **PDP** (Partial Dependence Plot), **ICE** (Individual Conditional Expectation), feature attribution heatmap.
- Mô hình interpretable-by-design: **ProtoPNet**, **Concept Bottleneck Models**.

---

## 6.4. Đánh giá diễn giải bằng dữ liệu thực nghiệm ⭐
- **"Does it work right?"** – kiểm chứng lời giải thích bằng dữ liệu thực nghiệm (ground truth sinh học).
- Áp dụng 5 chiều đánh giá (Fidelity/PGI, Interpretability, Robustness, Fairness, Completeness).
- **Dynamic Weighting** giữa các chiều tùy **domain**: Healthcare, Finance, Security có ưu tiên khác nhau.
- **Human-Centric / Human-Centered Evaluation**: đánh giá dựa trên con người ("Illustration of Understanding", benchmarking frameworks).

---

## 6.5. Xác định yếu tố sinh học chính trong mô hình AI ⭐
Hai góc nhìn (có so sánh với khoa học thần kinh):
- **Micro View**: 
  - **Receptive Fields vs Feature Visualization**.
  - **Knowledge Neuron** (neuron mang tri thức cụ thể).
  - Hạn chế: **Polysemanticity** (một neuron mã hóa nhiều khái niệm khác nhau → khó diễn giải).
- **Macro View**:
  - **Geometry of Thought**, **Distributed Representations** (biểu diễn phân tán trên nhiều neuron).
  - **Mechanistic Interpretability = Virtual Neuroscience**.
- **Behavioural View (Artificial Cognition)**: **Psychophysics for Machines**; case study **Shape Bias**.
- **Architectural / Bio-Inspired View**: 
  - **Beyond the Neuron: Astrocyte** (tế bào hình sao – vai trò tính toán ngoài neuron).
  - **Embodiment & Morphological Computation**, **Polycomputing & Xenobots**.

**Ứng dụng XAI trong tin sinh (từ bài coding):**
- **Gene expression analysis**: diễn giải tầm quan trọng của gene trong phân loại (vd loại ung thư).
- **Single-cell RNA-seq**: xác định marker chính.
- **Biomarker discovery**: feature selection + interpretation.
- **Protein structure/function**: attention maps (vd **AlphaFold** diễn giải attention nội bộ).
- **Drug response prediction**: diễn giải feature dự đoán đáp ứng điều trị.

---

## 6.6. Diễn giải trong các bài toán hiện đại (Healthcare focus) ⭐
- **Fidelity vs Fairness** (White-box Paradox).
- **Grad-CAM++** – phát hiện **khối u não (Brain Tumor Detection)** từ ảnh.
- **Beyond the Pixel: EMR (Electronic Medical Records)** – diễn giải trên hồ sơ y tế điện tử.
- **Mirror Effect: Saliency vs fMRI** – so bản đồ chú ý của AI với ảnh não người thật.
- **Neuroprosthetics & Interface**, **Astrocyte Revolution**, **Polycomputing & Xenobots**.

**Case studies (bài coding):**
1. Random Forest dự đoán subtype ung thư vú từ gene expression → diễn giải bằng **SHAP**.
2. Decision tree xác định nhóm bệnh nhân theo đột biến gen.
3. Diễn giải deep learning trong ảnh giải phẫu bệnh (pathology) → **CAM/Grad-CAM**.

**Thách thức XAI trong tin sinh:**
- **Biological noise vs signal** (nhiễu sinh học).
- **Correlation ≠ Causation** – feature "quan trọng" chưa chắc **nhân quả**.
- Data bias & model artifacts.
- Giải pháp mới nổi: **Causal inference**, interpretable deep models, **Responsible AI / Ethics**.

---

## 6.7. Câu hỏi ôn tập nhanh
1. Vì sao cần **XAI** trong tin sinh/y tế? Nêu lý do pháp lý.
2. Phân biệt **intrinsic vs post-hoc** interpretability. Cho ví dụ. Trade-off accuracy-interpretability?
3. Nêu **5 chiều đánh giá** một lời giải thích. **Fidelity** đo bằng gì (PGI)?
4. **The Disagreement Problem** là gì?
5. Thách thức riêng khi diễn giải **GenAI**? **Hallucination** & cách chống (RAG, uncertainty)?
6. So sánh **SHAP vs LIME vs Grad-CAM**. **Counterfactual explanation** là gì?
7. **Polysemanticity** và **distributed representation** là gì (Micro vs Macro view)?
8. Vì sao **correlation ≠ causation** quan trọng trong diễn giải biomarker?
