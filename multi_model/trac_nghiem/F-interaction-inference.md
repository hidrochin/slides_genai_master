# TRẮC NGHIỆM — Cụm F: Tương tác & Suy luận Đa thể thức (18 câu)
Nguồn: `Lecture7_1-MultimodalInteraction`, `Lecture7_2-MultimodalInference`.

> **Cách dùng:** Bốn phương án **ngắn, song song, dài cân bằng** — lý giải nằm ở đáp án ẩn. Chọn đáp án **trước**, rồi mở "Đáp án" xem **mổ xẻ từng phương án**. Câu **(Khó)** cần phân biệt bẫy; câu 🔗 nối kiến thức nhiều phần.

---

**Câu 1.** Bốn sub-challenge của Reasoning (Thách thức 3) là:
- A. Fusion, Coordination, Fission, và Alignment giữa các phần tử modality
- B. Structure modeling, Intermediate concepts, Inference paradigm, External knowledge
- C. Discrete, Continuous, Logical, và Causal theo cách suy luận trên bằng chứng
- D. Value function, Policy, Actor, và Critic trong khung reinforcement learning

<details><summary>Đáp án</summary>

**Đúng: B.** Structure / Concepts / Inference paradigm / Knowledge.
- **A sai:** đó là sub-challenge của Representation.
- **C sai:** đó là các *phân nhánh con* bên trong.
- **D sai:** đó là các thành phần của RL.
</details>

---

**Câu 2.** "Interactive structure" khác "temporal structure" ở điểm bản chất nào?
- A. Interactive hoàn toàn không có yếu tố thời gian, còn temporal thì có yếu tố đó
- B. Trong interactive, hành động ở bước trước ảnh hưởng đến trạng thái tương lai
- C. Temporal cần policy để chọn hành động, còn interactive thì lại không cần policy
- D. Interactive chỉ áp dụng cho dữ liệu văn bản, còn temporal cho dữ liệu hình ảnh

<details><summary>Đáp án</summary>

**Đúng: B.** Trong interactive, **action bước trước ảnh hưởng state tương lai** → cần policy, đưa vào **RL**.
- **A sai:** interactive *vẫn* có thời gian.
- **C sai:** đảo ngược — chính interactive mới cần policy.
- **D sai:** cả hai áp dụng cho nhiều modality.
</details>

---

**Câu 3.** Các phương pháp "exact" (value/policy iteration) chỉ áp dụng khi:
- A. Không gian state/action bất kỳ, ngay cả khi transition hoàn toàn chưa được biết
- B. Không gian state/action nhỏ & rời rạc, transition đã biết, MDP quan sát đầy đủ
- C. Chỉ cần biết hàm reward mà không cần biết gì về hàm transition của môi trường
- D. Không gian state là liên tục và cao chiều, cần dùng function approximation

<details><summary>Đáp án</summary>

**Đúng: B.** Exact methods lặp trên **mọi state-action** → cần **nhỏ, rời rạc** + transition **đã biết**.
- **A sai:** transition chưa biết → phải dùng Q-learning.
- **C sai:** value iteration *cần* transition.
- **D sai:** state liên tục cao chiều là chỗ exact *không* dùng được.
</details>

---

**Câu 4.** Vai trò của ε-greedy trong Q-learning là:
- A. Giảm learning rate theo thời gian để mô hình hội tụ mượt mà hơn về sau
- B. Cân bằng exploration và exploitation, giảm ε dần khi policy tốt dần lên
- C. Chuẩn hóa tất cả các giá trị Q về nằm trong khoảng đơn vị từ 0 đến 1
- D. Loại bỏ nhu cầu về hàm reward khi huấn luyện agent trong môi trường mới

<details><summary>Đáp án</summary>

**Đúng: B.** ε-greedy cân bằng **explore/exploit**, giảm ε dần khi học tốt hơn.
- **A sai:** ε điều khiển explore, không phải learning rate.
- **C sai:** không chuẩn hóa Q.
- **D sai:** RL *cần* reward.
</details>

---

**Câu 5. (Khó)** Deep Q-learning dễ phân kỳ vì hai lý do, được khắc phục bằng hai kỹ thuật tương ứng:
- A. Overfitting và underfitting; khắc phục bằng dropout và batch normalization
- B. Tương quan giữa mẫu và target không dừng; khắc phục bằng replay và fixed target
- C. Learning rate quá cao và quá thấp; khắc phục bằng một learning-rate scheduler
- D. Vanishing và exploding gradient; khắc phục bằng cách thay mạng bằng một LSTM

<details><summary>Đáp án</summary>

**Đúng: B.** DQN phân kỳ do (1) **tương quan giữa mẫu**, (2) **target không dừng** → **experience replay** + **fixed Q-targets**.
- **A, C, D sai:** đó là các vấn đề/kỹ thuật huấn luyện chung, không đặc thù DQN.
</details>

---

**Câu 6. 🔗** So với value-based methods, REINFORCE (policy gradient) có đặc điểm:
- A. Cần biết transition và ước lượng cả Q lẫn V, nhưng bù lại variance rất thấp
- B. Học trực tiếp policy, không cần transition, nhưng variance của ước lượng cao
- C. Luôn sample-efficient hơn value-based trên hầu hết mọi bài toán điều khiển
- D. Chỉ xử lý được action rời rạc chứ không dùng được cho action liên tục nào

<details><summary>Đáp án</summary>

**Đúng: B.** REINFORCE học **trực tiếp policy**, **không cần transition**, variance **cao**. Ước lượng gradient này tái dùng cho *generative models* ([cụm G](G-generation.md)).
- **A sai:** REINFORCE *không* cần transition/Q/V, variance *cao*.
- **C sai:** thường *kém* sample-efficient hơn.
- **D sai:** dùng được cho action liên tục.
</details>

---

**Câu 7.** Trong Actor-Critic, "advantage" thường dùng để giảm variance là:
- A. Reward thô của cả trajectory tính từ đầu đến cuối tập tương tác
- B. `Q(s,a) − V(s)` — action tốt hơn kỳ vọng của state bao nhiêu
- C. Learning rate nhân với reward tức thời nhận được ở mỗi bước
- D. Entropy của phân phối policy để khuyến khích việc khám phá thêm

<details><summary>Đáp án</summary>

**Đúng: B.** Advantage `Q(s,a) − V(s)`: action tốt hơn giá trị kỳ vọng của state bao nhiêu. **Actor** = policy, **Critic** = Q/V.
- **A sai:** reward thô là thứ gây variance cao mà baseline cần trừ.
- **C, D sai:** learning rate / entropy không phải định nghĩa advantage.
</details>

---

**Câu 8. 🔗** Trong instruction-following RL, vì sao "grounding" ngôn ngữ↔đối tượng quan trọng cho khái quát?
- A. Vì nó giúp tăng đáng kể tốc độ hội tụ của thuật toán value iteration
- B. Vì ground từ↔thuộc tính cho phép tổ hợp mới chưa thấy ("blue" + "pillar")
- C. Vì nó loại bỏ hoàn toàn nhu cầu về reward shaping trong quá trình học
- D. Vì nó biến bài toán reinforcement learning thành supervised learning thuần

<details><summary>Đáp án</summary>

**Đúng: B.** Grounding gắn (blue, pillar) với thuộc tính → **tổ hợp lại** nhận "blue pillar" chưa thấy (compositional generalization, nối Winoground ở [cụm A](A-tong-quan-6-thach-thuc.md)).
- **A sai:** không phải về tốc độ value iteration.
- **C sai:** grounding và reward shaping là hai hướng khác nhau.
- **D sai:** vẫn là RL.
</details>

---

**Câu 9.** Socratic Models (Zeng 2022) suy luận đa thể thức zero-shot bằng cách:
- A. Train một mô hình end-to-end duy nhất trên một tập dữ liệu ghép cặp khổng lồ
- B. Cho nhiều mô hình lớn trò chuyện theo kịch bản, mỗi cái góp tri thức miền riêng
- C. Dùng các hard attention gate 0/1 được huấn luyện bằng reinforcement learning
- D. Sinh ra một scene graph rồi chạy một neural state machine trên đồ thị đó

<details><summary>Đáp án</summary>

**Đúng: B.** Các foundation model **tương tác scripted, zero-shot**, mỗi cái có tri thức miền riêng; ngôn ngữ làm khái niệm trung gian.
- **A sai:** đặc điểm là *không* train chung.
- **C sai:** đó là discrete concepts via hard attention.
- **D sai:** đó là Neural State Machine.
</details>

---

**Câu 10.** VQA-LOL biến các toán tử logic AND/OR/NOT thành khả vi bằng:
- A. One-hot encoding các mệnh đề
- B. Fréchet inequalities (soft logic)
- C. Beam search trên cây suy luận
- D. K-means clustering các mệnh đề

<details><summary>Đáp án</summary>

**Đúng: B.** VQA-LOL dùng **Fréchet inequalities** làm soft logical operators khả vi.
- **A sai:** one-hot không làm logic khả vi.
- **C sai:** beam search là giải mã chuỗi.
- **D sai:** clustering không liên quan.
</details>

---

**Câu 11. (Khó)** Khác biệt cốt lõi giữa `p(y | do(x=3))` và `p(y | x=3)`:
- A. Chúng luôn bằng nhau miễn là ta có đủ dữ liệu quan sát để ước lượng
- B. `do` là phân phối can thiệp (ép X); `x=3` là quan sát; joint không đủ cho `do`
- C. `p(y|x=3)` đòi hỏi phải xóa các cạnh trong đồ thị nhân quả còn `do` thì không
- D. Toán tử `do` chỉ áp dụng được cho biến rời rạc chứ không cho biến liên tục

<details><summary>Đáp án</summary>

**Đúng: B.** `do(x=3)` = **can thiệp** (ép, "mutilate" đồ thị); `x=3` = **quan sát**; **joint distribution một mình không đủ** cho intervention.
- **A sai:** khác nhau khi có confounding, bất kể dữ liệu.
- **C sai:** đảo ngược — *intervention* mới xóa cạnh.
- **D sai:** `do` áp dụng cho cả biến liên tục.
</details>

---

**Câu 12.** Khi thực hiện intervention `do(X=x)` trên đồ thị nhân quả, thao tác đúng là:
- A. Thêm các cạnh mới đi từ X tới mọi biến khác ở trong đồ thị nhân quả
- B. Xóa tất cả các cạnh ĐI VÀO biến X ("mutilate" đồ thị nhân quả)
- C. Xóa tất cả các cạnh ĐI RA khỏi X để cắt tác động của X lên hậu quả
- D. Không thay đổi cấu trúc đồ thị, chỉ đơn giản là đặt giá trị mới cho X

<details><summary>Đáp án</summary>

**Đúng: B.** Intervention **xóa mọi cạnh đi vào** X (giữ cạnh đi ra).
- **A sai:** không thêm cạnh mới.
- **C sai:** xóa cạnh *đi ra* cắt đứt tác động của X lên Y — sai chiều.
- **D sai:** intervention *có* thay đổi cấu trúc.
</details>

---

**Câu 13.** Trong Causal VQA, "covariant editing" và "invariant editing" nhắm vào loại đối tượng nào?
- A. Covariant sửa đối tượng liên quan (treatment) → answer nên đổi; Invariant sửa vô quan → giữ
- B. Cả hai đều sửa đối tượng liên quan để buộc answer phải thay đổi theo mong đợi
- C. Covariant giữ nguyên answer sau khi sửa, còn Invariant lại làm answer thay đổi
- D. Cả hai đều không hề đụng đến ảnh, chỉ thay đổi cách diễn đạt của câu hỏi

<details><summary>Đáp án</summary>

**Đúng: A.** **Covariant** sửa **treatment** → answer *đổi*; **Invariant** sửa **nuisance** → answer *giữ*. Answer đổi khi sửa nuisance = bắt tương quan giả.
- **B sai:** invariant sửa đối tượng *vô quan*.
- **C sai:** đảo ngược kỳ vọng.
- **D sai:** cả hai *đều* chỉnh sửa ảnh.
</details>

---

**Câu 14.** OK-VQA (Marino 2019) đặt ra thách thức gì?
- A. VQA mà câu trả lời nằm hoàn toàn trong ảnh, không cần tới tri thức bên ngoài
- B. VQA đòi hỏi tri thức ngoài mà mô hình phải chủ động truy xuất để trả lời
- C. VQA chỉ với các câu hỏi dạng yes/no đơn giản không cần suy luận nhiều bước
- D. VQA không sử dụng ngôn ngữ, chỉ dựa hoàn toàn vào thông tin từ hình ảnh

<details><summary>Đáp án</summary>

**Đúng: B.** OK-VQA: câu hỏi **cần tri thức ngoài** → động lực cho KAT, knowledge graphs.
- **A sai:** ngược — *cần* tri thức ngoài.
- **C, D sai:** OK-VQA có câu hỏi phức tạp và dùng ngôn ngữ.
</details>

---

**Câu 15. 🔗** REINFORCE được coi là "giải pháp tối ưu ngẫu nhiên tổng quát" vì:
- A. Nó chỉ hoạt động được khi biến `z` liên tục và hàm `f` là khả vi trơn tru
- B. `z` rời rạc hoặc liên tục, `f(z)` hộp đen; dùng được cho cả NMN lẫn generative
- C. Nó luôn cho variance thấp nhất trong tất cả các phương pháp ước lượng gradient
- D. Nó yêu cầu phải biết trước transition probabilities của môi trường tương tác

<details><summary>Đáp án</summary>

**Đúng: B.** `z` rời rạc/liên tục, `f(z)` hộp đen → dùng cho **layout NMN** ([cụm E](E-transformers-reasoning.md), rời rạc) và **generative models** ([cụm G](G-generation.md)).
- **A sai:** đó là trường hợp *reparameterization* dùng được.
- **C sai:** variance thực ra *cao*.
- **D sai:** REINFORCE *không* cần transition.
</details>

---

**Câu 16.** DARTS (Differentiable Architecture Search) tăng tốc structure discovery bằng cách:
- A. Duyệt toàn bộ không gian kiến trúc rời rạc một cách vét cạn để tìm kiến trúc tốt
- B. Xấp xỉ lựa chọn bằng softmax (khả vi), giải bi-level optimization, rồi lấy argmax
- C. Dùng REINFORCE với reward là độ chính xác trên tập validation để chọn kiến trúc
- D. Dùng K-means clustering trên các kiến trúc ứng viên rồi chọn cụm tốt nhất trong đó

<details><summary>Đáp án</summary>

**Đúng: B.** DARTS xấp xỉ lựa chọn bằng **softmax** → giải **bi-level optimization** → argmax; nhanh hơn tìm kiếm rời rạc.
- **A sai:** DARTS *tránh* vét cạn rời rạc.
- **C sai:** đó là hướng NMN dùng RL.
- **D sai:** không dùng clustering.
</details>

---

**Câu 17. (Khó)** Trong "DAGs with NO TEARS", ràng buộc không chu trình được biến thành ràng buộc liên tục bằng:
- A. Duyệt DFS trên toàn bộ đồ thị để phát hiện có tồn tại chu trình nào hay không
- B. Kiểm tra trace của lũy thừa ma trận kề (đường chéo bằng 0 ⇒ không có chu trình)
- C. Sắp xếp topo các đỉnh của đồ thị rồi kiểm tra tính hợp lệ của thứ tự đó
- D. Đếm số cạnh của đồ thị rồi so sánh với tổng số đỉnh để suy ra tính chu trình

<details><summary>Đáp án</summary>

**Đúng: B.** NO TEARS: lũy thừa k của ma trận kề đếm **đường k-bước**; đường chéo mọi lũy thừa bằng 0 → không chu trình → **tối ưu liên tục** được.
- **A, C sai:** đó là thuật toán rời rạc (DFS/topo sort).
- **D sai:** đếm cạnh/đỉnh không xác định được chu trình.
</details>

---

**Câu 18. 🔗** "Discrete concept via hard attention" dùng cổng 0/1 rời rạc. Vì cổng rời rạc, mô hình được train thế nào?
- A. Bằng gradient thông thường qua toàn mạng, vì cổng 0/1 vẫn khả vi liên tục
- B. Bằng reinforcement learning (controller + reward), vì lựa chọn 0/1 không khả vi
- C. Bằng cách chuyển toàn bộ mạng sang bài toán optimal transport để tối ưu hóa
- D. Bằng cách thay hard attention bằng softmax rồi bỏ luôn tính chất rời rạc đi

<details><summary>Đáp án</summary>

**Đúng: B.** Cổng 0/1 rời rạc → train bằng **RL** (controller, reward = accuracy), cùng tinh thần REINFORCE (liên hệ gated fusion ở [cụm C](C-fusion-coordination-fission.md)).
- **A sai:** cổng 0/1 *không* khả vi trơn.
- **C sai:** OT không liên quan.
- **D sai:** đó là *bỏ* discrete concept.
</details>
