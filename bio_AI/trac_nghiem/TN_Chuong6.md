# Trắc nghiệm Chương 6 – Trí tuệ nhân tạo diễn giải (Explainable AI – XAI)

> ⚠️ **Nhiều đáp án đúng có thể xảy ra.** Tự làm rồi so với **ĐÁP ÁN** ở cuối file.

---

**Câu 1.** Vì sao cần **XAI** trong tin sinh/y tế?
- A. Quyết định rủi ro cao (chẩn đoán, khám phá thuốc)
- B. Lý do pháp lý/quy định (FDA, GDPR)
- C. Niềm tin & sự chấp nhận của bác sĩ/nhà sinh học
- D. Để tăng độ chính xác của mô hình lên 100%
- E. Vấn đề "black box": hiệu năng tăng thì diễn giải giảm

**Câu 2.** Phân biệt **intrinsic** và **post-hoc** interpretability?
- A. Intrinsic = mô hình tự dễ diễn giải (decision tree, linear model)
- B. Post-hoc = giải thích black-box sau khi huấn luyện
- C. SHAP, LIME, Grad-CAM là post-hoc
- D. Rule-based (RuleFit, RIPPER) là intrinsic
- E. Post-hoc = mô hình tự dễ diễn giải
- F. Có trade-off giữa accuracy và interpretability

**Câu 3.** Về **5 chiều đánh giá** một lời giải thích?
- A. Fidelity (trung thực – phản ánh chính xác hành vi mô hình gốc)
- B. Interpretability (con người có hiểu được không)
- C. Robustness (ổn định khi input bị nhiễu nhẹ)
- D. Fairness (công bằng)
- E. Completeness (đầy đủ)
- F. Fidelity đo bằng metric PGI (Prediction Gap on Importance)

**Câu 4.** Về **The Disagreement Problem**?
- A. Các phương pháp giải thích khác nhau cho kết quả mâu thuẫn nhau
- B. ABC, BND, PGI là các phương pháp/metric liên quan
- C. Là hiện tượng các mô hình luôn đồng ý với nhau
- D. Xảy ra khi giải thích cùng một dự đoán bằng nhiều phương pháp
- E. Chỉ xảy ra với mô hình intrinsic

**Câu 5.** Thách thức riêng khi diễn giải **GenAI**?
- A. Đầu ra biến thiên vô hạn (infinite output variability)
- B. Hallucination: đầu ra trôi chảy nhưng sai sự thật
- C. Cần prompt engineering control
- D. GenAI không bao giờ tạo ra thông tin sai
- E. Chống hallucination bằng Uncertainty Estimation và RAG

**Câu 6.** Ghép đúng **phương pháp diễn giải post-hoc**?
- A. SHAP dựa trên giá trị Shapley (lý thuyết trò chơi)
- B. LIME giải thích cục bộ (local)
- C. Grad-CAM/Grad-CAM++ tạo heatmap cho ảnh (CNN)
- D. Permutation importance đo tầm quan trọng feature
- E. Counterfactual explanation: "nếu input khác đi thì sao"
- F. SHAP chỉ giải thích được ở mức cục bộ, không toàn cục

**Câu 7.** Về **Micro View vs Macro View** trong diễn giải?
- A. Micro view: knowledge neuron, receptive fields
- B. Polysemanticity: một neuron mã hóa nhiều khái niệm (hạn chế của micro view)
- C. Macro view: distributed representations (biểu diễn phân tán)
- D. Mechanistic interpretability = virtual neuroscience
- E. Polysemanticity nghĩa là một neuron chỉ mã hóa một khái niệm duy nhất

**Câu 8.** Ứng dụng **XAI trong tin sinh** (bài coding)?
- A. Gene expression analysis (diễn giải gene quan trọng trong phân loại ung thư)
- B. Single-cell RNA-seq (xác định marker)
- C. Biomarker discovery
- D. AlphaFold diễn giải attention nội bộ trong dự đoán cấu trúc protein
- E. Drug response prediction

**Câu 9.** Thách thức XAI trong tin sinh?
- A. Biological noise vs signal (nhiễu sinh học)
- B. Correlation ≠ Causation (feature "quan trọng" chưa chắc nhân quả)
- C. Data bias & model artifacts
- D. Giải pháp: causal inference, interpretable deep models
- E. Feature quan trọng theo SHAP luôn là nguyên nhân gây bệnh

**Câu 10.** Diễn giải trong bài toán hiện đại (healthcare)?
- A. Grad-CAM++ phát hiện khối u não từ ảnh
- B. Diễn giải trên EMR (Electronic Medical Records)
- C. So sánh saliency map của AI với ảnh fMRI não người
- D. Case study: Random Forest + SHAP dự đoán subtype ung thư vú
- E. ProtoPNet và Concept Bottleneck Models là mô hình interpretable-by-design

---

## ✅ ĐÁP ÁN & GIẢI THÍCH

**1: A, B, C, E** — D sai (XAI không nhằm tăng accuracy lên 100%; thậm chí có trade-off).
**2: A, B, C, D, F** — E sai (post-hoc là giải thích *sau*, không phải tự diễn giải).
**3: A, B, C, D, E, F** — cả 6 đúng (5 chiều + Fidelity đo bằng PGI).
**4: A, B, D** — C sai (là hiện tượng *mâu thuẫn*, không đồng ý); E sai (không giới hạn ở intrinsic).
**5: A, B, C, E** — D sai (GenAI *có* tạo hallucination).
**6: A, B, C, D, E** — F sai (SHAP giải thích cả cục bộ *và* toàn cục).
**7: A, B, C, D** — E sai (polysemanticity = một neuron mã hóa *nhiều* khái niệm).
**8: A, B, C, D, E** — cả 5 đúng.
**9: A, B, C, D** — E sai (correlation ≠ causation → feature quan trọng *chưa chắc* là nguyên nhân).
**10: A, B, C, D, E** — cả 5 đúng.
