# ĐỀ THI THỬ — 50 câu trắc nghiệm tổng hợp (Chatbot & QA)

> Trộn toàn khoá. Tự bấm giờ ~50 phút. Đáp án + giải thích ngắn ở cuối.

---

**1.** Chatbot điền slot vào frame đến khi đủ để hành động là kiểu:
A. Rule-based  B. Frame-based  C. Generative  D. Search-based

**2.** RAG chatbot thuộc nhóm:
A. Retrieval-based thuần  B. Rule-based  C. Generative-based  D. Frame-based

**3.** Ba tác vụ lõi của NLU:
A. Intent, NER/slot, sentiment  B. Tokenize, stem, lemma  C. Retrieve, rank, generate  D. Chunk, embed, index

**4.** Nhãn BIO "I-" nghĩa là:
A. Bắt đầu thực thể  B. Bên trong thực thể  C. Ngoài thực thể  D. Không xác định

**5.** JointIDSF dùng cơ chế gì giữa soft intent embedding và token?
A. Convolution  B. Attention  C. Pooling  D. Dropout

**6.** Fine-tuning khác instruction-tuning:
A. Model lớn hơn  B. 1 tác vụ cụ thể, input→output, model nhỏ-vừa  C. Đa tác vụ qua prompt  D. Instruction→output

**7.** LoRA là:
A. Một LLM  B. Low-Rank Adapter (fine-tuning nhẹ)  C. Vector DB  D. Thuật toán retrieval

**8.** Back-translation là kỹ thuật:
A. Nén ngữ cảnh  B. Augmentation (dịch qua-lại)  C. Retrieval  D. Prompt

**9.** Thành phần RASA xác định action tiếp theo:
A. RASA NLU  B. RASA Core  C. Lookup Table  D. Tracker

**10.** Policy RASA dùng học sâu:
A. RulePolicy  B. MemoizationPolicy  C. TEDPolicy  D. FormPolicy

**11.** DIET học đồng thời:
A. Intent + entity + masked token  B. Intent + sentiment  C. NER + dịch  D. Retrieve + rerank

**12.** DIET so với BERT:
A. Chậm hơn  B. Nhanh gấp 6 lần, vượt trội  C. Bắt buộc pre-trained  D. Chỉ làm intent

**13.** File RASA KHÔNG dùng trực tiếp để train nhưng định nghĩa response/action:
A. nlu.yml  B. stories.yml  C. domain.yml  D. config.yml

**14.** Lookup Table trong RASA NLU dùng để:
A. Định nghĩa tập giá trị cho một slot  B. Cấu hình pipeline  C. Lưu story  D. Gọi API

**15.** MRC trả lời dựa trên:
A. Kho lớn  B. Một đoạn văn cụ thể  C. KG  D. CSDL

**16.** Trong SQuAD, answer là:
A. Câu sinh mới  B. Span trong đoạn  C. Yes/no  D. Số

**17.** BM25 là truy xuất:
A. Dense  B. Sparse/lexical  C. Multi-vector  D. Graph

**18.** Cross-encoder so với bi-encoder:
A. Chính xác hơn nhưng chậm hơn  B. Nhanh hơn  C. Precompute được  D. Không hiểu ngữ nghĩa

**19.** BGE-M3 nền tảng & max token:
A. BERT, 512  B. XLM-RoBERTa, 8192  C. GPT-2, 1024  D. T5, 2048

**20.** Multi-functionality của BGE-M3:
A. Dense + sparse + multi-vector  B. Chỉ dense  C. Chỉ tiếng Anh  D. Chỉ câu ngắn

**21.** RAG-Fusion khác Multi-Query ở:
A. Thêm re-ranker (chống lost-in-the-middle)  B. Không sinh biến thể  C. Dùng graph  D. Bỏ retriever

**22.** HyDE:
A. Sinh câu hỏi tổng quát  B. Sinh answer giả rồi embed  C. Chia sub-question  D. Route câu hỏi

**23.** CRAG khi không có tài liệu liên quan:
A. Trả lời "không biết"  B. Re-write câu hỏi → web search  C. Tăng chunk  D. Đổi model

**24.** Parent Document Retriever:
A. Embed chunk nhỏ, trả về doc cha  B. Dịch câu hỏi  C. Rerank  D. Nén prompt

**25.** Hai loại câu hỏi RAG thường FAIL:
A. Multi-hop & QFS  B. Yes/no & factoid  C. Definition & opinion  D. Procedural & comparative

**26.** GraphRAG thay vector DB bằng:
A. Knowledge Graph  B. BM25  C. Fine-tune  D. Cache

**27.** Thuật toán community detection của GraphRAG:
A. K-means  B. Leiden (phân cấp)  C. DBSCAN  D. Louvain thuần

**28.** Global search của GraphRAG dùng:
A. Map-Reduce trên community reports  B. Vector lookup  C. Regex  D. BM25

**29.** LightRAG giảm chi phí bằng cách bỏ:
A. Vector store  B. Hierarchical graph  C. LLM  D. Embedding

**30.** Dual-level retrieval của LightRAG:
A. Low-level (cụ thể) + High-level (trừu tượng)  B. Dense + sparse  C. Turn + session  D. Local + global cluster

**31.** HippoRAG 2 dùng thuật toán:
A. Personalized PageRank  B. Dijkstra  C. Beam search  D. A*

**32.** HippoRAG 2 cảm hứng từ:
A. Hippocampal indexing (trí nhớ người)  B. GAN  C. Transformer  D. Diffusion

**33.** Đơn vị nhớ tốt hơn turn/session theo slide:
A. Ký tự  B. Phân đoạn theo chủ đề  C. Toàn bộ lịch sử  D. Câu đơn

**34.** SeCom gồm:
A. Segmentation + Compression  B. Retriever + Generator  C. Encoder + Decoder  D. Map + Reduce

**35.** Công cụ nén token của SeCom:
A. LLMLingua-2  B. FAISS  C. BM25  D. spaCy

**36.** RMM cập nhật reranker bằng:
A. RL (reward = được LLM trích dẫn)  B. Supervised nhãn người  C. K-means  D. Regex

**37.** Ngưỡng MemTree θ(d)=θ₀e^(λd):
A. Càng sâu càng cao  B. Càng sâu càng thấp  C. Cố định  D. Ngẫu nhiên

**38.** Bốn thao tác của Mem0:
A. ADD/UPDATE/DELETE/NOOP  B. CRUD  C. PUSH/POP/PEEK/CLEAR  D. MAP/REDUCE/FILTER/SORT

**39.** MemGPT ví LLM như:
A. CPU của OS (RAM↔Disk, function call)  B. Database  C. Retriever  D. Compiler

**40.** Module MIRIX lưu mật khẩu/API key:
A. Core Memory  B. Episodic  C. Semantic  D. Knowledge Vault

**41.** Benchmark ~600 lượt, ~26k token/hội thoại:
A. SQuAD  B. LOCOMO  C. GLUE  D. MMLU

**42.** Metric tin cậy nhất cho QA hội thoại dài:
A. F1 thuần  B. LLM-as-a-Judge  C. Perplexity  D. Số token

**43.** Bốn thành phần của AI Agent:
A. Reasoner, Tools, Memory, Planner  B. Encoder, Decoder, Attn, FFN  C. Host, Client, Server, Transport  D. Retrieve, Rank, Gen, Index

**44.** Pattern mặc định của agent:
A. Plan-and-Execute  B. ReAct  C. Reflexion  D. Swarm

**45.** Ba primitive của LangGraph:
A. State, Node, Edge  B. Input, Process, Output  C. Prompt, Tool, Memory  D. Map, Reduce, Filter

**46.** Tính năng LangGraph dừng chờ người duyệt:
A. checkpointer  B. interrupt()  C. astream  D. compile()

**47.** MCP do ai phát triển & kết nối gì:
A. Anthropic, agent↔tool  B. Google, agent↔agent  C. OpenAI, agent↔user  D. Meta, agent↔model

**48.** Transport MCP dùng subprocess + stdin/stdout:
A. streamable-HTTP  B. stdio  C. WebSocket  D. gRPC

**49.** A2A object dùng để discover agent:
A. Task  B. Agent Card  C. Artifact  D. Message

**50.** MCP vs A2A:
A. MCP = vertical (agent–tool), A2A = horizontal (agent–agent)
B. MCP = agent–agent
C. Cả hai của Google
D. A2A thay MCP

---
### Đáp án & giải thích nhanh
1-B · 2-C · 3-A · 4-B (Inside) · 5-B · 6-B · 7-B · 8-B · 9-B · 10-C
11-A · 12-B · 13-C (domain.yml) · 14-A · 15-B · 16-B · 17-B · 18-A · 19-B · 20-A
21-A · 22-B · 23-B · 24-A · 25-A · 26-A · 27-B · 28-A · 29-B · 30-A
31-A · 32-A · 33-B · 34-A · 35-A · 36-A · 37-A · 38-A · 39-A · 40-D
41-B · 42-B · 43-A · 44-B · 45-A · 46-B · 47-A · 48-B · 49-B · 50-A

**Điểm dễ mất:**
- Câu 13: `domain.yml` KHÔNG train nhưng định nghĩa response/action; `nlu.yml` mới là file train.
- Câu 18: bi-encoder = retrieve (nhanh, precompute); cross-encoder = rerank (chính xác, chậm).
- Câu 21: Multi-Query KHÔNG rerank; RAG-Fusion CÓ rerank.
- Câu 28–30: GraphRAG (hierarchical + global map-reduce) vs LightRAG (bỏ hierarchical, dual-level).
- Câu 50: MCP vertical (agent–tool, Anthropic), A2A horizontal (agent–agent, Google).
