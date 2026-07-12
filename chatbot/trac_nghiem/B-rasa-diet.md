# Trắc nghiệm B — RASA & DIET

> Lý thuyết: [on_tap/B-rasa-diet](../on_tap/B-rasa-diet.md). Đáp án cuối file.

---

**1.** RASA là:
A. Dịch vụ đám mây trả phí của Google
B. Framework mã nguồn mở cho Conversational AI
C. Một mô hình LLM
D. Vector database

**2.** Thành phần RASA chịu trách nhiệm intent classification & entity extraction:
A. RASA Core  B. RASA NLU  C. RASA X  D. Action Server

**3.** Thành phần RASA quyết định action tiếp theo (quản lý luồng hội thoại):
A. RASA NLU  B. RASA Core  C. Tracker Store  D. Lookup Table

**4.** Tính năng RASA NLU định nghĩa một tập giá trị cho một slot (VD 64 tỉnh thành):
A. Regular Expression  B. Synonym  C. Lookup Table  D. Story

**5.** Policy nào của RASA Core dùng học sâu để xác định action?
A. RulePolicy  B. MemoizationPolicy  C. TEDPolicy  D. FallbackPolicy

**6.** Policy dùng các Story đã thấy để xác định action:
A. RulePolicy  B. MemoizationPolicy  C. TEDPolicy  D. FormPolicy

**7.** DIET viết tắt của:
A. Deep Intent Entity Transformer
B. Dual Intent and Entity Transformer
C. Distributed Inference Entity Trainer
D. Dynamic Intent Extraction Tool

**8.** DIET huấn luyện đồng thời ba tác vụ nào?
A. Intent, entity, masked token
B. Intent, sentiment, summarization
C. NER, translation, ranking
D. Retrieval, rerank, generation

**9.** Hàm loss của DIET là tổng của:
A. chỉ intent loss
B. L_intent + L_entity + L_masked
C. cross-entropy + MSE
D. contrastive loss đơn thuần

**10.** So với fine-tuned BERT, DIET được mô tả là:
A. Chậm hơn nhưng chính xác hơn
B. Vượt trội hơn và huấn luyện nhanh gấp 6 lần
C. Bắt buộc phải dùng pre-trained embeddings
D. Chỉ làm intent, không làm entity

**11.** Về pre-trained embeddings, DIET:
A. Bắt buộc dùng BERT embeddings
B. Cho phép tích hợp tùy chọn (BERT/GloVe/ConveRT), không bắt buộc
C. Không bao giờ dùng được embeddings ngoài
D. Chỉ dùng word2vec

**12.** DIET dùng cơ chế học nào thay cho MLM của BERT?
A. Reinforcement learning  B. Contrastive learning  C. Adversarial training  D. Knowledge distillation

**13.** Đặc trưng đầu vào "thưa" của DIET gồm:
A. one-hot token + multi-hot char n-gram
B. chỉ dense embeddings
C. TF-IDF thuần
D. positional encoding

**14.** File RASA định nghĩa intents/entities/responses/actions nhưng KHÔNG trực tiếp dùng để train:
A. nlu.yml  B. stories.yml  C. domain.yml  D. config.yml

**15.** File chứa dữ liệu huấn luyện intent/entity:
A. domain.yml  B. data/nlu.yml  C. config.yml  D. actions.py

**16.** File chứa kịch bản hội thoại để train mô hình hội thoại:
A. data/stories.yml  B. domain.yml  C. endpoints.yml  D. credentials.yml

**17.** File cấu hình pipeline xử lý NLP:
A. domain.yml  B. nlu.yml  C. config.yml  D. stories.yml

**18.** Khi cần gọi API/logic phức tạp, ta viết custom action vào:
A. domain.yml  B. actions/actions.py  C. nlu.yml  D. config.yml

**19.** Khi huấn luyện DIET với dữ liệu mới, cách tránh "quên" dữ liệu cũ:
A. Xoá toàn bộ dữ liệu cũ
B. Điều chỉnh learning rate hợp lý + transfer learning + trộn dữ liệu cũ-mới
C. Tăng learning rate thật cao
D. Chỉ train trên dữ liệu mới

**20.** Khi CHẠY chatbot, RASA dùng file nào để xác định intent & entity?
A. Pipeline trong config.yml  B. stories.yml  C. actions.py  D. credentials.yml

---
### Đáp án
1-B · 2-B · 3-B · 4-C · 5-C · 6-B · 7-B · 8-A · 9-B · 10-B · 11-B · 12-B · 13-A · 14-C · 15-B · 16-A · 17-C · 18-B · 19-B · 20-A
