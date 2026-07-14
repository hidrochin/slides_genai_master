# CHEAT-SHEET — Cụm F: Tương tác & Suy luận Đa thể thức (Thách thức 3 – Reasoning)
Nguồn: `Lecture7_1-MultimodalInteraction`, `Lecture7_2-MultimodalInference`. Đào sâu 4 sub-challenge của **Reasoning** + nền **Reinforcement Learning**.

> **Định nghĩa Reasoning:** *Kết hợp tri thức qua **nhiều bước suy luận**, khai thác **multimodal alignment** + cấu trúc bài toán.* **4 sub-challenge:** **A. Structure modeling** · **B. Intermediate concepts** · **C. Inference paradigm** · **D. External knowledge**.
> **Winoground nhắc lại:** CLIP/ViLT/ViLBERT ~ngẫu nhiên khi cần compositional generalization → 4 thành phần: structure, concepts, inference, knowledge.

---

## A. STRUCTURE MODELING — cấu trúc mà suy luận diễn ra trên đó
**Định nghĩa:** định nghĩa/học các quan hệ để suy luận. Trục: **single-step vs multi-step**; loại: **temporal, hierarchical, interactive, discovery**.

### A.1. Interactive structure → REINFORCEMENT LEARNING ⭐⭐
- **Khác temporal:** hành động ở bước trước **ảnh hưởng trạng thái tương lai** (policy `a`). Đưa đa thể thức vào khung RL.
- **MDP** = `(S, A, P(s'|s,a), r(s,a,s'), s0, γ, H)`. **RL vs Supervised:** RL = quyết định **tuần tự**, reward **tích lũy & thưa**, môi trường **có thể chưa biết**; SL = 1 bước, reward tức thời, giám sát dày.
- **Value/state functions:** `V^π(s)` (kỳ vọng reward từ s theo π); `Q^π(s,a)` (từ s, làm a rồi theo π). **Bellman optimality** (đệ quy).
- **Exact methods (MDP đã biết):** Value iteration, Policy iteration, Q-value iteration → hội tụ tới policy tối ưu. **Hạn chế:** cần **state/action nhỏ, rời rạc** + biết transition đầy đủ.
- **Q-learning (MDP chưa biết, model-free):** ước lượng ngầm transition qua **simulation/exploration**; **ε-greedy** (giảm ε dần) để cân bằng **exploration vs exploitation**.
- **Deep Q-learning (DQN):** xấp xỉ Q bằng mạng (state cao chiều, tổng quát hóa). **Diverges** với NN do: ① **tương quan giữa mẫu** ② **target không dừng (non-stationary)**. **Sửa:** **Experience replay** (lấy mini-batch ngẫu nhiên từ buffer → khử tương quan) + **Fixed Q-targets** (dùng tham số cũ `w⁻`, cập nhật mỗi ~1000 bước).
- **Policy gradients / REINFORCE ⭐:** học **trực tiếp policy**, **không cần transition probabilities**, không ước lượng Q/V. Gradient: nếu reward trajectory cao → **đẩy tăng** xác suất các action đã thấy; thấp → **đẩy giảm**. Nhược: **variance cao** (credit assignment khó).
- **Variance reduction — baseline:** trừ baseline `b(s)` (VD EMA reward) → quan trọng là reward **cao/thấp hơn kỳ vọng**.
- **Actor-Critic:** baseline tốt = **advantage `Q(s,a) − V(s)`**. **Actor** = policy (chọn action), **Critic** = Q/V (đánh giá) — kết hợp policy gradient + Q-learning.
- **Value-based vs Policy-based:** value-based (sample-efficient hơn, tôn trọng cấu trúc MDP, khó với continuous argmax) vs policy-based (trial-and-error hơn, đơn giản hơn, học trực tiếp policy, dễ diễn giải).

### A.2. Language + RL ⭐
- **Instruction following:** ngôn ngữ **chỉ định task**; **gated attention** (element-wise product) để ground ngôn ngữ↔đối tượng; **grounding quan trọng cho generalization** ("blue armor, red pillar" → "blue pillar" chưa thấy).
- **Embodied QA:** navigation + QA (Das 2018).
- **Language to rewards:** ngôn ngữ chỉ định **reward** thay vì action → **reward shaping** (Montezuma's Revenge — reward thưa/dài hạn), goal specification, preferences.
- **Language as domain knowledge:** đọc **manual/hướng dẫn** để chơi (Branavan 2012 — gán câu thành action/state/background).

### A.3. Structure Discovery ⭐
- **NMN end-to-end (Hu 2017):** RNN dự đoán **layout** → dùng **REINFORCE** (layout rời rạc, không reparameterizable).
- **REINFORCE như tối ưu ngẫu nhiên tổng quát:** `z` rời rạc **hoặc** liên tục; `f(z)` có thể là **hộp đen**; `q(z)` cần dễ lấy mẫu & khả vi theo tham số. → dùng cho cả structure discovery **và** generative models.
- **NAS (MUFASA):** tìm kiến trúc fusion tự động — **chậm** (discrete optimization).
- **DARTS (Liu 2019):** làm **khả vi** — xấp xỉ chọn bằng **softmax**, giải **bi-level optimization**, rồi softmax→argmax. Nhanh hơn nhưng vẫn không tầm thường.
- **DAGs with NO TEARS (Zheng 2018):** học cấu trúc DAG bằng **tối ưu liên tục**; ràng buộc **không chu trình** kiểm qua **trace của lũy thừa ma trận kề** (lũy thừa k đếm đường k-bước; đường chéo = 0 ⇒ không có chu trình k-bước). Nonconvex.

---

## B. INTERMEDIATE CONCEPTS — tham số hóa khái niệm đa thể thức
**Định nghĩa:** cách tham số hóa các khái niệm trung gian trong suy luận. **Discrete vs Continuous.**
- **Discrete via hard attention:** cổng **0/1** (thay vì softmax mềm) — tầng rời rạc chèn giữa các tầng khả vi; train bằng **RL** (controller + reward = accuracy). Dùng cho sentiment/emotion, image captioning.
- **Discrete via language — Socratic Models (Zeng 2022):** nhiều mô hình lớn (ngôn ngữ/video/audio) **trò chuyện với nhau**, mỗi model có domain knowledge riêng, tương tác **scripted & zero-shot** → captioning, robot planning, video reasoning. **Ngôn ngữ = khái niệm trung gian diễn giải được.**

---

## C. INFERENCE PARADIGM — suy ra khái niệm trừu tượng từ bằng chứng
**Vấn đề của fusion thuần:** bắt **tương quan giả (spurious)**, không robust với thao túng có chủ đích, thiếu diễn giải/kiểm soát. → cần paradigm **tường minh**.

### C.1. Logical inference ⭐
- **VQA-LOL (Gokhale 2020):** câu hỏi có **connective logic** AND/OR/NOT; mô hình hiện tại **kém** với logic. Giải: **soft logical operators** khả vi (dùng **Fréchet inequalities**) → toán tử AND/OR/NOT khả vi. Hướng mở: differentiable knowledge-base reasoning.

### C.2. Causal inference ⭐⭐ (rất hay hỏi)
- **Intervention `do(x)`:** kết quả nếu ta **ép** X (can thiệp), có thể trái với dữ liệu quan sát. **Association mô tả "sự thể như thế nào"; Causation mô tả "sẽ ra sao dưới hoàn cảnh khác".**
- **`p(y | do(x=3)) ≠ p(y | x=3)`** ⭐ — phân phối can thiệp ≠ phân phối điều kiện. **Chỉ dữ liệu joint là KHÔNG đủ** để dự đoán hành vi dưới can thiệp.
- **Causal diagram:** mũi tên cause→effect. **Intervention "mutilates" graph:** **xóa mọi cạnh ĐI VÀO** biến bị can thiệp. **Confounding variable** làm nhiễu (VD điều trị x ảnh hưởng bệnh y?). (Judea Pearl, *The Book of Why*.)
- **Causal VQA (Agarwal 2020):** model bắt causation hay correlation? **Covariant** editing (sửa **đối tượng liên quan** = treatment → `p(y|do(zebras=1))`) vs **Invariant** editing (sửa **đối tượng vô quan** = nuisance → answer nên **không đổi**). Thực hiện qua **data augmentation** (invariance + covariance).

---

## D. EXTERNAL KNOWLEDGE — dùng tri thức ngoài
**Định nghĩa:** khai thác tri thức ngoài trong nghiên cứu structure/concepts/inference.
- **OK-VQA (Marino 2019):** VQA **cần tri thức ngoài** ("what kind of board is this?" cần biết water sports). Mô hình hiện tại kém khi cần knowledge ngoài.
- **KAT (Knowledge Augmented Transformer, Gui 2022):** object detector → language model tra khái niệm → **multi-step retrieval**, composition neural.
- **Multimodal knowledge graphs:** suy luận multi-step, graph-based.
- **Commonsense knowledge:** **ATOMIC** (if-then), **Delphi** (moral), **Social Chemistry** (social/moral norms).

---

## 🎯 CÂU HAY RA THI (Cụm F)
1. 4 sub-challenge của Reasoning?
2. MDP gồm gì? Exact methods cần điều kiện gì? (state rời rạc nhỏ + biết transition).
3. Vì sao Deep Q-learning diverge, và 2 kỹ thuật sửa? (correlation + non-stationary target → experience replay + fixed Q-targets).
4. REINFORCE: cần biết transition không? Nhược điểm? Cách giảm variance? (không cần; variance cao; baseline → actor-critic advantage `Q−V`).
5. Actor vs Critic là gì?
6. `p(y|do(x))` khác `p(y|x)` thế nào? Intervention làm gì với đồ thị nhân quả? (xóa cạnh đi vào biến can thiệp).
7. Causal VQA: covariant vs invariant editing (treatment vs nuisance)?
8. VQA-LOL làm logic khả vi bằng gì? (Fréchet inequalities).
9. OK-VQA đặt vấn đề gì? KAT giải bằng gì?
10. REINFORCE dùng chung cho structure discovery và generative model vì sao? (z rời rạc/liên tục, f hộp đen).
