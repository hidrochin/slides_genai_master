# TRẮC NGHIỆM — Cụm G: Sinh Đa thể thức (18 câu)
Nguồn: `Lecture9.1-Generation-Part1`, `Lecture9.2-Generation-Part2`.

> **Cách dùng:** Bốn phương án **ngắn, song song, dài cân bằng** — lý giải nằm ở đáp án ẩn. Chọn đáp án **trước**, rồi mở "Đáp án" xem **mổ xẻ từng phương án**. Câu **(Khó)** cần suy luận; câu 🔗 nối kiến thức nhiều phần.

---

**Câu 1.** Xếp theo lượng content đầu ra: tóm tắt video, dịch text→ảnh, sinh đồng thời nhiều modality. Thứ tự đúng:
- A. Tóm tắt tăng content, dịch giữ nguyên content, sinh mới thì giảm content
- B. Tóm tắt giảm (reduction), dịch giữ (maintenance), sinh mới tăng (expansion)
- C. Cả ba đều giữ nguyên content, chỉ khác nhau ở modality của đầu ra sinh ra
- D. Tóm tắt giữ nguyên content, dịch tăng content, còn sinh mới thì giảm content

<details><summary>Đáp án</summary>

**Đúng: B.** Summarization = reduction, Translation = maintenance, Creation = expansion.
- **A, D sai:** đảo sai vai của tóm tắt/dịch/sinh.
- **C sai:** ba tác vụ khác nhau *ở lượng content*.
</details>

---

**Câu 2.** Trong chiều "generative process", exemplar và generative tương ứng:
- A. Exemplar ≈ abstractive (sinh mới); generative ≈ extractive (chọn mẫu)
- B. Exemplar ≈ extractive (chọn/truy xuất mẫu); generative ≈ abstractive (sinh mới)
- C. Cả hai đều là extractive, chỉ khác nhau ở độ dài của đầu ra cuối cùng
- D. Cả hai đều là abstractive, chỉ khác nhau ở modality của đầu ra sinh ra

<details><summary>Đáp án</summary>

**Đúng: B.** Exemplar = chọn mẫu ≈ **extractive**; generative = sinh mới ≈ **abstractive**.
- **A sai:** đảo ngược.
- **C, D sai:** hai kiểu *khác* bản chất.
</details>

---

**Câu 3.** DALL-E (2021) và DALL-E 2 (2022) sinh ảnh bằng hai cách khác nhau. Cặp mô tả đúng:
- A. DALL-E dùng CLIP + diffusion; DALL-E 2 dùng dVAE + autoregressive transformer
- B. DALL-E dùng dVAE/VQ-VAE + autoregressive; DALL-E 2 dùng CLIP + diffusion
- C. Cả hai bản đều dùng GAN với một discriminator để phân biệt ảnh thật và giả
- D. Cả hai bản đều dùng normalizing flow trực tiếp trên không gian pixel của ảnh

<details><summary>Đáp án</summary>

**Đúng: B.** DALL-E: **dVAE + autoregressive**; DALL-E 2: **CLIP + diffusion**.
- **A sai:** đảo ngược hai bản.
- **C, D sai:** cả hai *không* dùng GAN hay normalizing flow.
</details>

---

**Câu 4. (Khó)** Vì sao ước lượng maximum likelihood trực tiếp cho VAE là intractable?
- A. Vì mạng nơ-ron encoder của VAE quá lớn để có thể tối ưu một cách hiệu quả
- B. Vì marginal `p(x)=∫p(x,z)dz` cần tổng/tích phân trên toàn bộ latent z
- C. Vì không có đủ dữ liệu huấn luyện để ước lượng phân phối hậu nghiệm p(z|x)
- D. Vì biến latent z luôn được quan sát trực tiếp nên không cần phải suy diễn ra

<details><summary>Đáp án</summary>

**Đúng: B.** Marginal likelihood cần **tích phân/tổng trên toàn bộ z** (2³⁰ số hạng nếu z 30-bit; tích phân bất khả nếu liên tục).
- **A sai:** kích thước encoder không phải lý do.
- **C sai:** vấn đề là *tính tích phân*, không phải thiếu dữ liệu.
- **D sai:** z **không** được quan sát.
</details>

---

**Câu 5.** ELBO của VAE gồm hai số hạng nào?
- A. Cross-entropy và perplexity, dùng để đo độ chính xác của việc dự đoán
- B. Reconstruction `E_q[log p(x|z)]` và regularization `−KL(q(z|x)‖p(z))`
- C. Policy gradient và baseline, dùng để giảm variance của ước lượng gradient
- D. Forward noise và reverse noise, tương ứng với thêm và khử nhiễu dần dần

<details><summary>Đáp án</summary>

**Đúng: B.** Reconstruction (decoder) − KL regularization (giữ q gần prior).
- **A sai:** không phải hai thành phần ELBO.
- **C sai:** đó là RL.
- **D sai:** đó là diffusion.
</details>

---

**Câu 6. (Khó) 🔗** Reparameterization trick `z = μ + σ⊙ε` (ε~N(0,I)) có mục đích và điều kiện:
- A. Làm z trở nên rời rạc để có thể áp dụng được thuật toán REINFORCE
- B. Tách ε khỏi tham số để gradient chảy qua kỳ vọng; cần z liên tục, f khả vi
- C. Loại bỏ hoàn toàn tính ngẫu nhiên ra khỏi mô hình để việc train ổn định hơn
- D. Tăng variance của ước lượng gradient nhằm khuyến khích mô hình khám phá thêm

<details><summary>Đáp án</summary>

**Đúng: B.** Đưa randomness vào ε độc lập → `z` khả vi theo φ. Cần z liên tục, q reparameterizable, f khả vi; khi rời rạc/hộp đen → **REINFORCE** ([cụm F](F-interaction-inference.md)).
- **A sai:** reparameterization dành cho z *liên tục*.
- **C sai:** nó *giữ* ngẫu nhiên, chỉ tách ra.
- **D sai:** nó *giảm* variance.
</details>

---

**Câu 7. 🔗** Khi nào phải dùng REINFORCE thay cho reparameterization trick?
- A. Khi biến `z` liên tục và hàm `f` khả vi trơn tru theo tham số của nó
- B. Khi `z` rời rạc hoặc `f(z)` là hộp đen (không reparameterizable/khả vi)
- C. Khi cần huấn luyện mô hình nhanh hơn trên phần cứng tăng tốc như GPU
- D. Khi có sẵn dữ liệu ghép cặp giữa hai modality để giám sát quá trình học

<details><summary>Đáp án</summary>

**Đúng: B.** z rời rạc (action RL, layout NMN) hoặc f hộp đen → **REINFORCE**.
- **A sai:** đó là chỗ reparameterization dùng được.
- **C sai:** tốc độ không phải tiêu chí.
- **D sai:** ghép cặp không liên quan.
</details>

---

**Câu 8.** β-VAE với β > 1 nhằm mục đích gì?
- A. Khôi phục lại VAE chuẩn với trọng số của số hạng KL bằng đúng giá trị 1
- B. Tăng trọng số KL để ép các chiều latent độc lập hơn (disentanglement)
- C. Tăng độ mờ của ảnh sinh ra nhằm giảm hiện tượng overfitting của mô hình
- D. Bỏ hẳn số hạng reconstruction trong ELBO để chỉ tập trung tối ưu prior

<details><summary>Đáp án</summary>

**Đúng: B.** β>1 tăng trọng số KL → chiều latent **độc lập hơn (disentangled)**.
- **A sai:** β=1 mới là VAE chuẩn.
- **C sai:** mục tiêu là disentanglement.
- **D sai:** β điều chỉnh KL, không bỏ reconstruction.
</details>

---

**Câu 9. (Khó)** Diffusion model khác VAE ở ba điểm nào?
- A. Latent dim nhỏ hơn data; encoder được học từ dữ liệu; không hề có prior
- B. Latent dim bằng data; encoder KHÔNG học (Gaussian định sẵn); tham số biến thiên theo t
- C. Không dùng ELBO; không hề có bước reverse; chỉ có một quá trình forward
- D. Chỉ dùng cho text; và luôn cho ảnh sắc nét hơn hẳn autoregressive model

<details><summary>Đáp án</summary>

**Đúng: B.** Latent dim = data dim; encoder q **cố định** (Gaussian định sẵn); tham số Gaussian biến thiên theo t → là "multi-level VAE".
- **A sai:** ngược cả ba điểm.
- **C sai:** diffusion *có* ELBO và reverse.
- **D sai:** diffusion dùng cho ảnh/nhiều modality.
</details>

---

**Câu 10.** Latent Diffusion (Stable Diffusion) nhanh hơn diffusion trên pixel nhờ:
- A. Bỏ hoàn toàn quá trình khử nhiễu để rút ngắn thời gian sinh ảnh đầu ra
- B. Chạy diffusion trong không gian latent (autoencoder nén, diffusion trên latent)
- C. Giảm số bước thêm nhiễu xuống đúng còn một nửa so với diffusion pixel gốc
- D. Bỏ text encoder để tiết kiệm chi phí tính toán khi điều kiện trên văn bản

<details><summary>Đáp án</summary>

**Đúng: B.** Diffusion trong **không gian latent** (nhỏ hơn pixel): autoencoder nén tri giác, diffusion nén ngữ nghĩa.
- **A sai:** vẫn có khử nhiễu.
- **C sai:** không phải giảm số bước "một nửa".
- **D sai:** vẫn dùng text encoder.
</details>

---

**Câu 11.** Classifier-free guidance (GLIDE) so với classifier guidance có ưu điểm:
- A. Cần train một classifier riêng trên dữ liệu nhiễu ở mọi mức thời gian khuếch tán
- B. Dùng một model duy nhất, train uncond bằng set y=const; thực nghiệm ưa dùng hơn
- C. Không thể điều kiện được trên văn bản mà chỉ điều kiện được trên nhãn lớp rời rạc
- D. Chỉ hoạt động được với mô hình VAE chứ không dùng được với mô hình diffusion

<details><summary>Đáp án</summary>

**Đúng: B.** Classifier-free: **một model**, train uncond = set y=const → không cần classifier riêng; GLIDE ưa dùng hơn.
- **A sai:** đó là *classifier* guidance.
- **C sai:** classifier-free điều kiện được cả text.
- **D sai:** nó là kỹ thuật *của* diffusion.
</details>

---

**Câu 12.** So sánh ba họ mô hình sinh, phát biểu nào đúng?
- A. Autoregressive: exact likelihood, chậm sample; VAE: train nhanh, ảnh mờ; Diffusion: chất lượng cao, chậm sample
- B. VAE cho chất lượng ảnh cao nhất và tốc độ sample nhanh nhất trong cả ba họ mô hình
- C. Diffusion cho exact likelihood và sample rất nhanh nhờ mô hình hóa quá trình nhiễu
- D. Autoregressive dễ điều kiện nhất và tốc độ sample nhanh nhất nhờ tính song song hóa

<details><summary>Đáp án</summary>

**Đúng: A.** Autoregressive exact/chậm sample; VAE train nhanh/mờ; Diffusion chất lượng cao/chậm sample.
- **B sai:** VAE cho ảnh *mờ*.
- **C sai:** diffusion *không* exact và sample *chậm*.
- **D sai:** autoregressive *khó* condition và sample *chậm* (tuần tự).
</details>

---

**Câu 13.** Autoregressive models (PixelRNN, WaveNet, GPT) có đặc điểm chung:
- A. Sinh ra toàn bộ đầu ra một cách song song chỉ trong duy nhất một bước forward
- B. Phân rã `p(x)=Π p(x_i|x_{<i})` → exact likelihood; nhưng sample tuần tự nên chậm
- C. Hoàn toàn không cho phép tính được likelihood chính xác của một mẫu dữ liệu
- D. Không thể nào điều kiện được trên bất kỳ thông tin bên ngoài nào khi sinh ra

<details><summary>Đáp án</summary>

**Đúng: B.** Chain rule → **exact likelihood**; sample tuần tự chậm.
- **A sai:** sinh *tuần tự*.
- **C sai:** chúng *có* exact likelihood.
- **D sai:** có thể condition (chỉ là "không dễ").
</details>

---

**Câu 14.** Sub-challenge Creation (4c) khó nhất vì:
- A. Chỉ phải sinh ra một modality duy nhất từ một modality nguồn cho trước
- B. Phải sinh đồng thời nhiều modality, tăng content, giữ mạch lạc trong và giữa modality
- C. Không cần bất kỳ tương tác chéo nào giữa các modality khi sinh dữ liệu mới
- D. Chỉ đơn giản là truy xuất một mẫu có sẵn từ trong tập dữ liệu huấn luyện

<details><summary>Đáp án</summary>

**Đúng: B.** Sinh **đồng thời nhiều modality**, tăng content, giữ mạch lạc trong & giữa modality → tổng hợp representation/alignment/reasoning.
- **A sai:** đó là Translation.
- **C sai:** Creation *cần* tương tác chéo.
- **D sai:** đó là exemplar.
</details>

---

**Câu 15. 🔗** "Conditioning via prefix tuning" của Frozen (2021) hoạt động thế nào?
- A. Fine-tune lại toàn bộ language model trên dữ liệu đa thể thức đã ghép cặp sẵn
- B. Giữ LM đóng băng, train một image encoder/adapter tạo prefix để điều kiện LM
- C. Train một diffusion model hoàn toàn từ đầu để có thể sinh ra được văn bản mới
- D. Dùng classifier-free guidance để điều khiển đầu ra text của language model đó

<details><summary>Đáp án</summary>

**Đúng: B.** Frozen giữ **LM đóng băng**, học adapter/prefix từ ảnh → điều kiện LM (cũng là **transfer via pretrained**, [cụm H](H-transference.md)).
- **A sai:** điểm mấu chốt là *không* fine-tune toàn bộ.
- **C sai:** không train diffusion cho text.
- **D sai:** classifier-free là cho diffusion.
</details>

---

**Câu 16.** Trong ba góc nhìn về captioning, "captioning as translation" tương ứng:
- A. Truy xuất triplet `<object, action, scene>` rồi lấy về một câu mô tả có sẵn
- B. Dùng câu template mô tả các object/attribute/relation đã phát hiện (Baby Talk)
- C. Visual storytelling sinh ra một câu chuyện sáng tạo gồm nhiều câu liên tiếp nhau
- D. Tóm tắt trừu tượng một đoạn video How2 thành một đoạn văn bản ngắn gọn hơn

<details><summary>Đáp án</summary>

**Đúng: B.** Captioning as translation = **câu template** mô tả object/attribute/relation (Baby Talk).
- **A sai:** đó là as summarization.
- **C sai:** đó là as generation.
- **D sai:** đó là tóm tắt video.
</details>

---

**Câu 17. (Khó)** Diffusion model dạng liên tục (phương trình vi phân / SDE) có thể được diễn giải là:
- A. Một mô hình autoregressive với chain rule chính xác trên từng chiều dữ liệu
- B. Một mô hình latent variable "vô hạn tầng", mẫu chất lượng cao, exact log-likelihood
- C. Một GAN với vô hạn discriminator được huấn luyện đối kháng đồng thời với nhau
- D. Một VAE với latent dim bằng 1 và một encoder tuyến tính đơn giản duy nhất

<details><summary>Đáp án</summary>

**Đúng: B.** Diffusion liên tục (SDE) = **mô hình latent "vô hạn tầng"** → mẫu chất lượng cao, exact log-likelihood, controllable.
- **A sai:** autoregressive khác diffusion liên tục.
- **C sai:** diffusion không phải GAN.
- **D sai:** latent dim = data dim, không phải 1.
</details>

---

**Câu 18. 🔗** Creation được nêu là "recall representation & alignment, recall reasoning". Vì sao?
- A. Vì Creation thực chất chỉ là một tên gọi khác của thách thức Fusion mà thôi
- B. Vì để mạch lạc chéo modality, nó cần biểu diễn/căn chỉnh tốt và cấu trúc suy luận
- C. Vì Creation không liên quan gì tới các thách thức khác, nó chỉ dùng diffusion thôi
- D. Vì Creation chỉ cần dùng tới Quantification để đo lường chất lượng đầu ra sinh ra

<details><summary>Đáp án</summary>

**Đúng: B.** Creation cần **representation/alignment** ([cụm C/D](D-alignment.md)) để nội dung khớp, và **reasoning** ([cụm E/F](F-interaction-inference.md)) cho cấu trúc temporal/causal.
- **A sai:** Creation là sub-challenge của Generation.
- **C sai:** nó *phụ thuộc mạnh* vào các thách thức khác.
- **D sai:** Quantification là đo lường, không tạo mạch lạc.
</details>
