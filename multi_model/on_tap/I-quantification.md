# CHEAT-SHEET — Cụm I: Lượng hóa (Thách thức 6 – Quantification)
Nguồn: `lecture12.2-quantification`. Nghiên cứu **thực nghiệm & lý thuyết** để hiểu heterogeneity, interactions, learning process. (Bài này cũng **tổng kết cả 6 thách thức**.)

> **Định nghĩa Quantification:** *Nghiên cứu thực nghiệm & lý thuyết để hiểu rõ hơn **heterogeneity, cross-modal interactions, và tiến trình học** đa thể thức.* **3 sub-challenge:** **6a Heterogeneity** · **6b Connections & Interactions** · **6c Learning process**.

---

## 6a. HETEROGENEITY ⭐
**Định nghĩa:** lượng hóa **6 chiều heterogeneity** (element representation, element distribution, structure, information, noise, relevance — xem [A](A-tong-quan-6-thach-thuc.md)) và ảnh hưởng của chúng lên modeling/learning.
- **Modality biases:** unimodal bias & **modality collapse** → cần **balancing modalities/training** (VQA v2 "Making the V matter", greedy learning, impartial optimization cho VAE).
- **Social biases (fairness):** ① unimodal (image captioning bắt tương quan giả **gender↔action** — "Women also Snowboard"); ② **cross-modal interactions làm bias TỆ HƠN** (thông tin thị giác khiến model **tự tin hơn** củng cố định kiến — "Worst of Both Worlds").
- **Noise & robustness:** modality-specific robustness; **missing modalities** → tradeoff mạnh performance↔robustness (MultiBench). Sửa: robust training, **suy diễn modality thiếu** (translation/joint-prob model, cyclic residual autoencoder).
- **Quantify heterogeneity via transfer (HighMMT):** ước lượng **ma trận heterogeneity của modality & interaction** (qua pretrained + few-shot transfer, ẩn chứa 6 chiều) → **parameter clustering** (chia sẻ tham số giữa modality/interaction giống nhau) → tìm **Pareto front** trên >10,000 tổ hợp model.

---

## 6b. CONNECTIONS & INTERACTIONS ⭐⭐⭐ (trọng tâm nhất)

**Connections** (tĩnh, có sẵn trong dữ liệu): Association (correlation/co-occurrence) · Dependency (causal/temporal) · Correspondence (grounding) · Relationship (function) — mức **stronger/weaker/unconnected**.

**Interactions** (khi inference): hiểu **cách các modality kết hợp** cung cấp thông tin cho task. Ba loại (PID):
- **Redundancy (R):** thông tin **chung** cả hai modality có về task (VD "This movie is great!" cả text & visual đều dương).
- **Uniqueness (U1, U2):** thông tin **riêng** mỗi modality.
- **Synergy (S):** thông tin **trồi lên** chỉ khi kết hợp (VD **sarcasm**: "wowww" + giọng chán = mỉa mai).

### 6b.1. Khung PID định lượng Synergy ⭐⭐ (Liang 2023)
- **Định nghĩa Synergy toán học:**
  `Synergy = (thông tin đa thể thức GỐC về task) − (thông tin đa thể thức từ phân phối "tệ nhất" ghép cùng 2 unimodal marginals)`.
- `q` phải là **coupling** của hai unimodal marginals (giữ nguyên marginal, đổi cách ghép). Đây là **partial information decomposition** (Bertschinger 2014).
- **Ước lượng:**
  - `X1,X2,Y` **rời rạc nhỏ** → nghiệm chính xác bằng **convex programming** (CVXPY), tương đương **max-entropy optimization**.
  - **cao chiều/liên tục** → **neural network estimator** (thuật toán **Sinkhorn** không chuẩn hóa).
- **Ứng dụng:** ① **quantify dataset** (sentiment/sarcasm/VQA có bao nhiêu R/U/S); ② **model selection** (interaction polytope → chọn model >96% performance, VD sarcasm→Multimodal Transformer, VQA→Multiplicative); ③ mental health (mood từ text+keystroke); ④ computational pathology (histology+genomics).

### 6b.2. Định lượng cross-modal interactions của MÔ HÌNH đã train ⭐
- **Định nghĩa thống kê (Friedman 2008):** `f` có tương tác giữa `x_A, x_B` **iff** `f` **KHÔNG** phân rã được thành `f_A(x_A) + f_B(x_B)` (non-additive).
- **EMAP (Hessel & Lee 2020):** `μ` = đo **tổng lượng cross-modal interaction** (chiếu f về additive `f̂`; nếu `f̂ = f` → không có tương tác non-additive).
- **MultiViz (Liang 2023):** tương tác cá thể qua **đạo hàm bậc 2** `∂²f/∂x_A∂x_B > 0` (mở rộng bậc 2 của gradient-based).
- **Phân loại theo unimodal importance `I_A, I_B`:** `I_A·I_B > 0` → **complementary**; `I_A·I_B < 0` → **conflict**; `I_A ≫ I_B` → **dominance** (⭐ **ngôn ngữ thường áp đảo** trong sentiment analysis). Dùng GradCAM/LIME/SHAP; công cụ M2Lens, VL-InterpreT.

### 6b.3. Đánh giá việc quantification ⭐
- **Vấn đề:** dataset/model thực **không có nhãn interaction** sẵn.
- **Direct evaluation:** tạo **synthetic dataset** cho từng loại R/U1/U2/S (interaction polytope) — nhưng giới hạn ở synthetic.
- **Indirect evaluation:** ① **model simulation** (con người có tái tạo dự đoán model với accuracy/agreement cao không? MultiViz stages → accuracy tăng 55→81.7%); ② **model debugging** (con người tìm & sửa bug — VD "model bắt cross-modal interaction nhưng fail nhận màu" → thêm ví dụ về màu → +30.5%); ③ model/data selection theo quantification.
- **Open challenges:** **faithfulness** (giải thích có phản ánh đúng cơ chế nội tại?), **usefulness**, **disagreement** (các phương pháp giải thích khác nhau cho kết quả khác nhau).

---

## 6c. LEARNING PROCESS ⭐
**Định nghĩa:** đặc trưng hóa các thách thức **học & tối ưu** khi học từ dữ liệu dị thể.
- **Vấn đề:** thêm modality **không phải lúc nào cũng giúp** (Kinetics: RGB+Audio+OpticalFlow). Hai lý do: ① mạng đa thể thức **phức tạp hơn → dễ overfit**; ② các modality **overfit/generalize khác tốc độ** (greedy learning).
- **OGR (Overfitting-to-Generalization Ratio):** đo gap train↔valid loss cho từng modality → biết **train modality nào bao nhiêu**. **Ý tưởng:** train song song mạng đơn thể thức để ước lượng OGR → **reweight loss đa thể thức** cân bằng generalization/overfitting.
- **Open:** học/tổng quát/tối ưu ở `p ≫ n`; **modality shortcuts & biases**; giảm chiều, chọn modality, model compression.

---

## TỔNG KẾT 6 THÁCH THỨC (bài này chốt cả môn) ⭐⭐
| # | Thách thức | Một câu |
|---|---|---|
| 1 | **Representation** | học biểu diễn phản ánh tương tác chéo (Fusion/Coordination/Fission) |
| 2 | **Alignment** | mô hình hóa kết nối chéo giữa mọi phần tử (Discrete/Continuous/Contextualized) |
| 3 | **Reasoning** | kết hợp tri thức qua nhiều bước (Structure/Concepts/Inference/Knowledge) |
| 4 | **Generation** | sinh raw modality giữ mạch lạc (Summarization/Translation/Creation) |
| 5 | **Transference** | chuyển tri thức giúp modality yếu (Transfer/Co-learning/Model Induction) |
| 6 | **Quantification** | hiểu heterogeneity/interactions/learning |

**Multimodal = khoa học về dữ liệu Heterogeneous + Connected + Interacting.**
**Hướng tương lai:** heterogeneity (beyond additive, causal/logical), **high-modality** (MultiBench, non-parallel, low-resource), long-term (compositionality, memory, personalization), interaction (social intelligence, causality, ethical), real-world (healthcare, fairness, robustness).

---

## 🎯 CÂU HAY RA THI (Cụm I)
1. 3 sub-challenge của Quantification?
2. 3 loại interaction (R/U/S)? Synergy tương ứng ví dụ gì? (sarcasm, emergence).
3. Định nghĩa Synergy theo PID (gốc − phân phối tệ nhất ghép marginals). Ước lượng rời rạc vs liên tục? (convex programming/CVXPY vs neural/Sinkhorn).
4. Định nghĩa thống kê "có tương tác" (không phân rã được thành f_A+f_B). EMAP đo gì (μ)?
5. Phân loại complementary/conflict/dominance theo `I_A·I_B`? Modality nào thường áp đảo sentiment?
6. Direct vs indirect evaluation của quantification? (synthetic R/U/S vs model simulation/debugging).
7. Vì sao thêm modality không luôn giúp? OGR là gì và dùng thế nào?
8. Cross-modal interactions làm social bias tốt hơn hay tệ hơn? (tệ hơn — worst of both worlds).
