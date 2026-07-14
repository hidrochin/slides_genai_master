# TRẮC NGHIỆM — Cụm I: Lượng hóa (Quantification) (16 câu)
Nguồn: `lecture12.2-quantification`. (Cụm này tổng hợp cả 6 thách thức — nhiều câu 🔗.)

> **Cách dùng:** Bốn phương án **ngắn, song song, dài cân bằng** — lý giải nằm ở đáp án ẩn. Chọn đáp án **trước**, rồi mở "Đáp án" xem **mổ xẻ từng phương án**. Câu **(Khó)** cần phân biệt bẫy; câu 🔗 nối kiến thức nhiều phần.

---

**Câu 1.** So với năm thách thức xây-dựng-mô-hình còn lại, Quantification khác biệt ở mục tiêu:
- A. Sinh ra dữ liệu đa thể thức hoàn toàn mới với chất lượng cao và mạch lạc chéo
- B. Nghiên cứu thực nghiệm & lý thuyết để hiểu heterogeneity, interactions, learning
- C. Căn chỉnh các phần tử giữa những modality khác nhau dựa vào cấu trúc dữ liệu
- D. Chuyển giao tri thức từ một modality mạnh sang một modality yếu về tài nguyên

<details><summary>Đáp án</summary>

**Đúng: B.** Quantification = **hiểu/phân tích/đo lường** heterogeneity, interactions, learning.
- **A sai:** đó là Generation.
- **C sai:** đó là Alignment.
- **D sai:** đó là Transference.
</details>

---

**Câu 2. 🔗** Ba loại tương tác đa thể thức trong khung PID là:
- A. Additive, Multiplicative, và Nonlinear theo cơ chế toán học kết hợp modality
- B. Redundancy, Uniqueness, và Synergy theo cách thông tin đóng góp cho task
- C. Early, Late, và Hybrid fusion theo thời điểm hai modality được kết hợp lại
- D. Association, Dependency, và Correspondence theo loại kết nối giữa modality

<details><summary>Đáp án</summary>

**Đúng: B.** Redundancy, Uniqueness, Synergy (cùng khung PID ở [cụm C](C-fusion-coordination-fission.md)).
- **A sai:** đó là *cơ chế* fusion.
- **C sai:** đó là góc nhìn thời điểm fusion.
- **D sai:** đó là các loại *connection*.
</details>

---

**Câu 3.** Ví dụ điển hình của Synergy (thông tin trồi lên) là:
- A. "This movie is great!" — cả text và visual đều cùng hướng dương tính về task
- B. Sarcasm — lời khen "wowww" cộng giọng chán tạo nghĩa mỉa mai không có riêng lẻ
- C. Nhận diện đối tượng chỉ từ ảnh mà không cần dùng đến bất kỳ modality nào khác
- D. Dịch một câu văn bản đầu vào sang một bức ảnh tương ứng với nội dung câu đó

<details><summary>Đáp án</summary>

**Đúng: B.** Sarcasm = thông tin **emergent** chỉ khi kết hợp.
- **A sai:** đó là redundancy.
- **C sai:** đó là uniqueness.
- **D sai:** đó là translation (Generation).
</details>

---

**Câu 4. (Khó)** Trong khung PID (Liang 2023), Synergy được định nghĩa toán học là:
- A. Tổng mutual information của từng modality riêng lẻ với biến task Y cần dự đoán
- B. Thông tin GỐC về task trừ thông tin từ phân phối "tệ nhất" ghép cùng hai marginals
- C. Hiệu số entropy giữa modality thứ nhất và modality thứ hai trong bài toán học
- D. Tích của mutual information giữa hai modality với nhau khi cùng dự đoán task Y

<details><summary>Đáp án</summary>

**Đúng: B.** `Synergy = I_gốc(đa thể thức về task) − I(phân phối tệ nhất ghép cùng 2 marginals)`. `q` là coupling giữ nguyên marginals.
- **A sai:** tổng MI đơn thể thức không tách được synergy.
- **C, D sai:** hiệu entropy / tích MI không phải định nghĩa synergy.
</details>

---

**Câu 5.** Để ước lượng PID khi rời rạc nhỏ, và khi cao chiều liên tục, ta dùng lần lượt:
- A. Convex programming (CVXPY) và neural network estimator (Sinkhorn)
- B. Beam search và greedy search trên không gian trạng thái tương ứng
- C. K-means clustering và thuật toán phân cụm DBSCAN cho dữ liệu nhiễu
- D. Value iteration và policy iteration trong khung MDP đã biết đầy đủ

<details><summary>Đáp án</summary>

**Đúng: A.** Rời rạc nhỏ → **convex programming** (CVXPY); cao chiều/liên tục → **neural estimator** (Sinkhorn).
- **B sai:** đó là giải mã chuỗi.
- **C sai:** clustering không ước lượng PID.
- **D sai:** đó là RL.
</details>

---

**Câu 6. 🔗** Định nghĩa thống kê "mô hình `f` có tương tác chéo giữa `x_A` và `x_B`" (Friedman 2008):
- A. Khi `f` có thể phân rã được thành tổng `f_A(x_A) + f_B(x_B)` của hai hàm con
- B. Khi `f` KHÔNG phân rã được thành tổng `f_A(x_A) + f_B(x_B)` (non-additive)
- C. Khi giá trị của `x_A` bằng đúng với giá trị của `x_B` trên toàn miền dữ liệu
- D. Khi `f` là một hàm tuyến tính của cả hai biến `x_A` và `x_B` cùng một lúc

<details><summary>Đáp án</summary>

**Đúng: B.** Có tương tác **iff không phân rã được** thành `f_A + f_B` → **non-additive** (nền của EMAP ở [cụm C](C-fusion-coordination-fission.md)).
- **A sai:** phân rã được = *không* có tương tác.
- **C, D sai:** bằng nhau / tuyến tính không phải định nghĩa tương tác.
</details>

---

**Câu 7. 🔗** EMAP (Hessel & Lee 2020) đo đại lượng `μ` biểu thị:
- A. Giá trị perplexity của một mô hình ngôn ngữ trên tập dữ liệu kiểm tra đích
- B. Tổng lượng cross-modal interaction trên một mô hình + dataset đã được train
- C. Giá trị learning rate tối ưu để huấn luyện một mạng fusion cho hội tụ nhanh
- D. Tổng số tham số của mạng fusion được dùng để kết hợp các modality lại với nhau

<details><summary>Đáp án</summary>

**Đúng: B.** `μ` đo **tổng lượng tương tác chéo**; nếu `f̂=f` thì không có tương tác non-additive.
- **A, C, D sai:** perplexity / learning rate / số tham số không phải thứ EMAP đo.
</details>

---

**Câu 8.** MultiViz nhận diện tương tác chéo cá thể giữa hai đặc trưng bằng:
- A. Đạo hàm bậc nhất `∂f/∂x_A` của mô hình theo một trong hai đặc trưng đầu vào
- B. Đạo hàm bậc hai chéo `∂²f/∂x_A∂x_B > 0` giữa hai đặc trưng của hai modality
- C. Trace của ma trận kề đồ thị tính toán được từ cấu trúc bên trong của mô hình
- D. Trọng số softmax của lớp attention cuối cùng trong kiến trúc của mô hình đó

<details><summary>Đáp án</summary>

**Đúng: B.** **Đạo hàm bậc hai chéo** `∂²f/∂x_A∂x_B > 0` (mở rộng bậc 2 của gradient, liên hệ Grad-CAM ở [cụm B](B-bieu-dien-don-the-thuc.md)).
- **A sai:** bậc nhất đo *importance*, không đo tương tác.
- **C sai:** trace ma trận kề là của NO TEARS.
- **D sai:** softmax attention không phải cách đo này.
</details>

---

**Câu 9.** Theo unimodal importance `I_A, I_B`, khi `I_A · I_B < 0` thì tương tác là:
- A. Complementary (bổ sung) — hai modality cùng hướng và cùng củng cố kết luận
- B. Conflict (xung đột) — hai modality ngược hướng nhau trong việc dự đoán task
- C. Dominance (áp đảo) — một modality có importance lớn hơn hẳn modality còn lại
- D. Redundancy (dư thừa) — hai modality mang thông tin trùng lặp nhau về cùng task

<details><summary>Đáp án</summary>

**Đúng: B.** `I_A·I_B>0` → complementary; `<0` → **conflict**; `I_A≫I_B` → dominance (ngôn ngữ thường áp đảo sentiment).
- **A sai:** complementary ứng với tích *dương*.
- **C sai:** dominance ứng với importance *lớn hơn hẳn*, không phải dấu tích.
- **D sai:** redundancy không phân loại bằng dấu `I_A·I_B`.
</details>

---

**Câu 10. 🔗** Phát biểu nào ĐÚNG về social bias trong Quantification?
- A. Việc kết hợp thị giác và ngôn ngữ luôn luôn làm giảm thiên lệch xã hội có sẵn
- B. Tương tác chéo modality có thể khuếch đại bias — thị giác làm mô hình tự tin hơn
- C. Thiên lệch chỉ tồn tại ở modality ngôn ngữ, còn thị giác thì luôn luôn trung tính
- D. Image captioning không bao giờ học được tương quan giả giữa gender và action

<details><summary>Đáp án</summary>

**Đúng: B.** Tương tác chéo **khuếch đại bias** ("Worst of Both Worlds", "Women also Snowboard") — nhắc lại [cụm A](A-tong-quan-6-thach-thuc.md).
- **A, C, D sai:** đều trái với phát hiện thực nghiệm.
</details>

---

**Câu 11. 🔗** HighMMT lượng hóa heterogeneity nhằm:
- A. Sinh ra các bức ảnh có chất lượng cao từ nhiều modality đầu vào khác nhau
- B. Xác định cách chia sẻ tham số (parameter clustering) giữa modality tương đồng
- C. Tính toán giá trị perplexity của một mô hình ngôn ngữ đa thể thức trên tập test
- D. Căn chỉnh trục thời gian giữa tín hiệu âm thanh và tín hiệu hình ảnh của video

<details><summary>Đáp án</summary>

**Đúng: B.** Ước lượng ma trận heterogeneity → **parameter clustering** (chia sẻ tham số giữa modality/interaction tương đồng) — liên hệ [cụm C](C-fusion-coordination-fission.md).
- **A sai:** HighMMT không phải mô hình sinh ảnh.
- **C sai:** không phải tính perplexity.
- **D sai:** căn thời gian là Alignment.
</details>

---

**Câu 12. 🔗** Vì sao thêm modality không phải lúc nào cũng cải thiện hiệu năng (Wang 2020)?
- A. Vì mọi modality luôn dư thừa thông tin của nhau nên thêm vào chỉ gây nhiễu loạn
- B. Vì mạng đa thể thức dễ overfit hơn, và các modality generalize khác tốc độ nhau
- C. Vì mutual information giữa các modality luôn luôn bằng 0 nên không kết hợp được
- D. Vì thiếu position embedding khiến mô hình không phân biệt được các modality khác

<details><summary>Đáp án</summary>

**Đúng: B.** (1) mô hình phức tạp → **dễ overfit**; (2) modality **overfit/generalize khác tốc độ** (greedy learning) → giải bằng OGR.
- **A sai:** không "luôn dư thừa".
- **C sai:** MI thường >0.
- **D sai:** position embedding không liên quan.
</details>

---

**Câu 13.** OGR (Overfitting-to-Generalization Ratio) được dùng thế nào?
- A. Đo perplexity của từng modality rồi chọn ra modality có perplexity thấp nhất
- B. Đo gap train↔valid loss theo từng modality → biết train mỗi cái bao nhiêu, reweight
- C. Chọn learning rate tối ưu cho toàn mô hình bằng cách grid search trên tập valid
- D. Nén mô hình đa thể thức để giảm thời gian huấn luyện và bộ nhớ khi triển khai

<details><summary>Đáp án</summary>

**Đúng: B.** OGR đo **gap train↔valid loss** theo từng modality → **reweight loss** đa thể thức cân bằng generalization/overfitting.
- **A sai:** OGR không phải perplexity.
- **C, D sai:** OGR không phải để chọn learning rate hay nén mô hình.
</details>

---

**Câu 14.** "Model simulation" trong đánh giá gián tiếp quantification nghĩa là:
- A. Chạy mô phỏng Monte Carlo trên trọng số của mô hình để ước lượng độ bất định
- B. Kiểm tra xem con người, nhờ giải thích, có tái tạo được dự đoán của mô hình không
- C. Tạo ra dữ liệu synthetic cho từng loại redundancy/uniqueness/synergy để kiểm chứng
- D. Đo tốc độ inference của mô hình trên phần cứng đích để đánh giá hiệu quả triển khai

<details><summary>Đáp án</summary>

**Đúng: B.** Nếu giải thích tốt thì **con người tái tạo được dự đoán** với accuracy/agreement cao (MultiViz 55→81.7%).
- **A sai:** không phải Monte Carlo.
- **C sai:** đó là *direct* evaluation.
- **D sai:** tốc độ inference không phải model simulation.
</details>

---

**Câu 15.** Direct evaluation của quantification bị giới hạn ở điểm nào?
- A. Chỉ dùng được trên dữ liệu synthetic, vì dataset thực không có nhãn interaction sẵn
- B. Không thể tạo được dữ liệu redundancy hay synergy để đem đi kiểm tra mô hình
- C. Luôn luôn cần con người ngồi gán nhãn thủ công cho từng mẫu dữ liệu thực tế
- D. Không thể nào đo được thành phần uniqueness của mỗi modality riêng lẻ trong task

<details><summary>Đáp án</summary>

**Đúng: A.** Dataset thực **không có nhãn interaction** → phải tạo **synthetic** cho R/U/S → **giới hạn ở synthetic**.
- **B sai:** synthetic *tạo được* R/U/S.
- **C sai:** synthetic sinh có kiểm soát, không cần gán nhãn tay.
- **D sai:** synthetic đo được cả uniqueness.
</details>

---

**Câu 16. (Khó)** Đâu là một open challenge của việc quantify interactions / giải thích mô hình?
- A. Faithfulness — giải thích có phản ánh đúng cơ chế nội tại của mô hình hay không
- B. Mọi mô hình hiện nay luôn cho ra giải thích trung thực một cách tuyệt đối chính xác
- C. Mọi phương pháp giải thích khác nhau đều luôn cho ra cùng một kết quả giống hệt
- D. Không hề tồn tại cách nào để tạo ra được dữ liệu synthetic phục vụ việc kiểm chứng

<details><summary>Đáp án</summary>

**Đúng: A.** Open challenges: **faithfulness**, **usefulness**, **disagreement**.
- **B, C sai:** chính vì giải thích *không* luôn trung thực/nhất quán nên mới là thách thức.
- **D sai:** synthetic data *tạo được*.
</details>
