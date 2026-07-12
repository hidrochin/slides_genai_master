# B — Xây dựng chatbot với RASA & kiến trúc DIET

> Bài 3. ⇐ [ONE-PAGER](00-ONE-PAGER.md) · liên quan [A-tong-quan-nlu](A-tong-quan-nlu.md)

---

## 1. RASA là gì
Framework **mã nguồn mở** cho Conversational AI, dễ tùy chỉnh/mở rộng/triển khai.
Tính năng nổi bật: huấn luyện bằng **dữ liệu riêng**; tùy chỉnh hoàn toàn (không phụ thuộc bên thứ ba); tích hợp FB/Telegram/Zalo/Web; **hỗ trợ tiếng Việt**; kết hợp ML **hoặc** rule-based; **bảo mật** (không gửi dữ liệu ra ngoài).

## 2. Hai thành phần lõi của RASA

### 2.1 RASA NLU (hiểu ngôn ngữ)
Xử lý câu người dùng: **tokenize → featurize → Intent Classification + Entity Extraction**.
Tính năng bổ trợ:
- **Regular Expression**: trích thực thể bằng regex (ngày tháng, từ khoá).
- **Synonym**: từ đồng nghĩa ("ub", "ubnd" → "Ủy ban nhân dân").
- **Lookup Table**: tập giá trị cho 1 slot (VD 64 tỉnh thành → gặp "Hải Phòng" tự gán slot Province).

### 2.2 RASA Core (quản lý luồng hội thoại)
Quyết định **action** tiếp theo. Tập hợp các policy = **Dialog Policies**:
| Policy | Cơ chế |
|---|---|
| **RulePolicy** | dùng **luật** để xác định action |
| **MemoizationPolicy** | dùng **Story** (kịch bản đã thấy) để xác định action |
| **TEDPolicy** | dùng **học sâu** (deep learning) để xác định action |

> **Bẫy:** MemoizationPolicy dựa trên **stories**; TEDPolicy dựa trên **deep learning**; RulePolicy dựa trên **rules**.

## 3. Kiến trúc DIET (Dual Intent and Entity Transformer)
DIET Classifier: **nhẹ, hiệu quả, vượt trội BERT, huấn luyện nhanh gấp 6 lần**.

### 3.1 Huấn luyện DIET — 3 tác vụ ĐỒNG THỜI
1. Dự đoán **intent**.
2. Trích **entity**.
3. Dự đoán **masked token** (1 token bị mask ngẫu nhiên → model đoán → kéo các từ gần nghĩa lại gần nhau trong không gian ngữ nghĩa).

**Hàm loss:** `L = L_I + L_E + L_M` (intent + entity + masked token).

### 3.2 Vì sao DIET > fine-tuned BERT & nhanh gấp 6 lần ⭐ (6 lý do)
1. **Transformer nhẹ**, tối ưu cho intent+entity; không xử lý toàn bộ vector ngữ cảnh như BERT.
2. **Đặc trưng thưa**: one-hot token + multi-hot **char n-gram**; không bắt buộc pre-trained embeddings.
3. **Linh hoạt pre-trained embeddings** (BERT/GloVe/ConveRT) — **tùy chọn, không bắt buộc**; kể cả không dùng vẫn tốt nhất.
4. **Contrastive Learning** thay vì MLM → tối ưu trực tiếp cho intent+entity.
5. **End-to-end Multi-task** (intent + entity cùng lúc); BERT phải fine-tune riêng từng tác vụ.
6. **Hiệu suất tính toán cao**: ít tham số, ít tính toán → train nhanh.

### 3.3 Cách cải tiến DIET
1. **Train với dữ liệu mới**: trộn dữ liệu cũ + mới; transfer learning; điều chỉnh **learning rate** để tránh **quên** dữ liệu cũ (catastrophic forgetting).
2. **Thêm pre-trained embeddings** để tăng tính tổng quát.
3. **Tuning kiến trúc**: tăng số lớp Transformer / attention heads; dropout regularization; đổi activation.
4. **Kỹ thuật nâng cao**: contrastive learning; multi-task learning.

## 4. Các bước tạo chatbot với RASA
1. Cài môi trường (Python 3.8/3.9, tạo venv, `pip install rasa`).
2. `rasa init` → tạo thư mục project.
3. **Các file quan trọng** ⭐:

| File | Vai trò |
|---|---|
| **domain.yml** | định nghĩa intents, entities, **responses**, actions. **KHÔNG trực tiếp train**; cho chatbot biết cách phản hồi |
| **data/nlu.yml** | dữ liệu **train** intent/entity ( `[Hà Nội](location)` = entity) |
| **data/stories.yml** | **kịch bản** hội thoại (train mô hình hội thoại) |
| **config.yml** | cấu hình **pipeline** xử lý NLP |
| **actions/actions.py** | **custom action** (gọi API, logic phức tạp) |

4. Tạo dữ liệu train → 5. `rasa train` → 6. `rasa shell` chạy chatbot.
7. Custom Action: thêm vào `actions.py`, cập nhật `domain.yml`, chạy **action server**.
8. Triển khai: tích hợp Telegram/Messenger hoặc REST API.

**Luồng khi TRAIN:** đọc `config.yml` (pipeline) → `nlu.yml` (train intent/entity) → `stories.yml` (train hội thoại) → `domain.yml` (biết intent/response/action) → lưu vào `models/`.
**Luồng khi CHẠY:** user nhập → pipeline (`config.yml`) xác định intent+entity → kiểm tra `domain.yml` có response/action → nếu cần action gọi `actions.py` → trả lời.

---
## ✅ Chốt nhanh mục B
- RASA = NLU (tokenize/featurize/intent/entity + Regex/Synonym/**Lookup Table**) + Core (**RulePolicy/MemoizationPolicy/TEDPolicy**).
- **DIET** = 3 tác vụ đồng thời (intent + entity + **masked token**), loss `L_I+L_E+L_M`.
- DIET > BERT, **nhanh 6×**: đặc trưng thưa, pre-trained tùy chọn, **contrastive** (không MLM), end-to-end multi-task.
- File: **domain.yml (không train)** vs **nlu.yml (train)** vs stories.yml (kịch bản) vs config.yml (pipeline) vs actions.py.
