# ONE-PAGER — Ôn nước rút Chatbot & QA (liếc trước giờ thi)

**Thi trắc nghiệm (multiple-choice), phủ M1–M2.** Toàn khoá: Tổng quan → NLU → RASA → QA/RAG → GraphRAG/LightRAG → Quản lý bộ nhớ → Agent/MCP.
Chi tiết: [A-tong-quan-nlu](A-tong-quan-nlu.md) · [B-rasa-diet](B-rasa-diet.md) · [C-qa-rag](C-qa-rag.md) · [D-graphrag-lightrag](D-graphrag-lightrag.md) · [E-quan-ly-bo-nho](E-quan-ly-bo-nho.md) · [F-agent-mcp](F-agent-mcp.md)

---

## 🧩 PHÂN LOẠI CHATBOT (dễ bị lừa)
- **Rule-based** = IF keyword THEN reply · **Frame-based** = điền slot vào frame, đầy frame → hành động.
- **AI-based** chia 2: **Retrieval-based** (chọn câu trả lời có sẵn) vs **Generative-based** (LLM sinh câu trả lời).
- Retrieval-based 3 kiểu: **NLP-based** (intent + slot + CSDL) · **Search-based** (search engine) · **Knowledge-based** (KB/KG).
- Generative: General · Fine-tuned · **RAG** · Multi-modal · Personalized.

## 🗣️ NLU — 3 tác vụ lõi
**Intent detection** (hiểu mục đích) · **NER/Slot filling** (trích thực thể, nhãn **BIO**) · **Sentiment**.
- 3 tầng phương pháp cho cả 3 tác vụ: **Rule → ML → Deep Learning** (+ Zero/Few-shot LLM cho sentiment).
- ML intent: vector hoá (**BoW, TF-IDF, word2vec, BERT**) + classifier (**SVM, RF, LogReg, Naive Bayes**).
- DL: RNN/LSTM/GRU, **BERT/PhoBERT**. NER-DL: **BiLSTM+CRF**, **BERT+Softmax/CRF**.
- **JointIDSF**: học chung intent+slot; `[CLS]`→intent (softmax) → **soft intent embedding** → attention với token → slot decoder (**CRF**).
- BIO: `B-` bắt đầu thực thể, `I-` bên trong, `O` ngoài.

## 🚀 Nâng chất chatbot bằng LLM
| Kỹ thuật | Điểm nhớ |
|---|---|
| **Fine-tuning** | 1 tác vụ cụ thể, input→output, model **nhỏ-vừa (100M–7B)**, rẻ, phải train riêng từng tác vụ |
| **Instruction-tuning** | đa tác vụ qua prompt, instruction→output, model **lớn (7B–70B+)**, đa năng, tốn tài nguyên |
| **Prompt Engineering** | Zero-shot / One-shot / Few-shot / **Chain-of-Thought** |
| **Adapter / LoRA** | chỉ train vài layer chèn thêm, giữ nguyên trọng số gốc → nhẹ (HF **PEFT**). LoRA = Low-Rank Adapter |
| **Data Augmentation** | Paraphrase · **Back-translation** · Template · Entity swapping · Synthetic-LLM |
| **Context-aware** | session history · **sliding window** · summarization (T5/BART) · **DST** (dialogue state tracking) |

## 🤖 RASA & DIET
- **RASA NLU** (tokenize→featurize→intent+entity; Regex/Synonym/**Lookup Table**) + **RASA Core** (Dialog Policies: **RulePolicy · MemoizationPolicy · TEDPolicy**).
- File: **domain.yml** (intents/entities/responses/actions – KHÔNG train) · **nlu.yml** (train intent/entity) · **stories.yml** (kịch bản) · **config.yml** (pipeline) · **actions.py** (custom action).
- **DIET** = Dual Intent and Entity Transformer. Học **đồng thời 3 tác vụ**: intent + entity + **masked token**. Loss = `L_I + L_E + L_M`.
- DIET **> fine-tuned BERT, nhanh gấp 6 lần**: transformer nhẹ, đặc trưng thưa (one-hot token + char n-gram), pre-trained embeddings **tùy chọn (không bắt buộc)**, **contrastive loss** (không dùng MLM), đa nhiệm end-to-end.

## 🔎 QA & RETRIEVAL
- QA: factoid, yes/no, definition, cause, procedural, comparative… · **MRC** = đọc-hiểu 1 đoạn (**SQuAD** ~100k, answer = span). **Open-domain** = tìm trên kho lớn (Wikipedia).
- **BM25** = sparse/lexical (giống TF-IDF + chuẩn hoá độ dài); nhanh nhưng **không hiểu ngữ nghĩa**, giả định từ độc lập.
- **Bi-encoder** = mã hoá Q và D **độc lập** → so cosine; nhanh, **precompute embeddings** (dùng để retrieve). **Cross-encoder** = ghép Q+D vào 1 model; **chính xác hơn, chậm hơn** (dùng để **re-rank**).
- **BGE-M3**: nền **XLM-RoBERTa**, max **8192 token**; **Multi-lingual · Multi-functionality** (dense + sparse/lexical + multi-vector) **· Multi-granularity**; **self-knowledge distillation**.

## 🧠 ADVANCED RAG (thứ tự pipeline)
**Query Translation → Routing → Query Construction → Indexing → Retrieval → Generation**
- **Query Translation**: Multi-Query (nhiều biến thể) · **RAG-Fusion** (+re-ranker, chống *lost-in-the-middle*) · Decomposition (sub-question) · **Step-back** (câu hỏi tổng quát hơn) · **HyDE** (sinh câu trả lời giả rồi embed).
- **Indexing**: fixed-size chunk (chunk lớn = nhiều ngữ cảnh + nhiều nhiễu) · **Parent Document Retriever** (embed chunk nhỏ, trả về doc cha).
- **Generation**: chống *lost-in-the-middle* & dư thừa → **Reranking (ColBERT)** + **context compression**. **CRAG** (grade doc → web search nếu kém) · **Self-RAG** (tự phản tỉnh/critique).

## 🕸️ GRAPHRAG → LIGHTRAG → HIPPORAG2
- RAG thường **fail** ở: **multi-hop reasoning** & **query-focused summarization (QFS)**. GraphRAG dựng **KG** thay vì vector DB.
- **GraphRAG (Local→Global)**: chunk → LLM trích **entity + relationship** (có description + strength) → build graph → **Leiden** community detection (phân cấp) → **community summaries** → **Global search = Map-Reduce** (map: mỗi community sinh điểm + score; reduce: gộp). **Local search** cho câu hỏi cụ thể.
- **LightRAG**: **bỏ hierarchical graph** (rẻ hơn, thích ứng dữ liệu mới nhanh) · **dual-level retrieval**: **low-level** (thực thể cụ thể) + **high-level** (chủ đề trừu tượng); trích **high/low-level keywords**; kết hợp graph + vector.
- **HippoRAG 2**: cảm hứng **hippocampal indexing**; OpenIE triples + **passage nodes** (dense) + phrase nodes (sparse) + **Personalized PageRank**; query-to-triple thay NER-to-node.

## 💾 QUẢN LÝ BỘ NHỚ (memory ≈ RAG cho hội thoại)
- Vì sao cần: nhất quán · cá nhân hoá · theo dõi tác vụ · tối ưu token. Đơn vị: **turn < session**; phân đoạn theo **chủ đề** tốt hơn.
- **Loại memory**: Core · Episodic · Semantic · Procedural · Resource · Knowledge Vault (MIRIX 6 loại).
- **SeCom** = **SE**gmentation (chia theo chủ đề, GPT-4) + **COM**pression (nén = khử nhiễu, **LLMLingua-2**).
- **RMM**: Prospective (tóm tắt→chủ đề) + Retrospective (reranker học bằng **RL**, reward = LLM có trích dẫn memory không).
- **MemTree**: cây động; nút = {content, embedding, parent-child, depth}; **ngưỡng thích ứng θ(d)=θ₀e^(λd)**; **Collapsed Tree Retrieval**.
- **Mem0**: chỉ giữ **fact** cốt lõi; 4 thao tác **ADD/UPDATE/DELETE/NOOP**. **Mem0g** = graph (Neo4j). **MemGPT**: LLM như **OS**, main context (RAM) ↔ external (disk), **paging** qua function call.
- **MIRIX** (đa tác nhân, 6 module, Meta Memory Manager) — SOTA LOCOMO (**J Score 85.4**).
- Benchmark: **LOCOMO** (600 lượt/26k token; single/multi-hop/temporal/open) · Long-MT-Bench+ · LongMemEval (s/m) · **MSC**. Metric: F1/BLEU/ROUGE/BERTScore + **LLM-as-a-Judge**; retrieval: **Recall@k, NDCG@k**.

## 🦾 AGENT · LANGGRAPH · MCP · A2A
- **Agent** = Perceive → Reason → Act → Observe (loop). Thành phần: **Reasoner (LLM) · Tools · Memory · Planner**.
- Patterns: **ReAct** (Thought→Action→Observation, mặc định) · **Plan-and-Execute** (lập kế hoạch trước) · **Reflexion** (self-critique) · Tree-of-Thoughts · ReWOO.
- **LangChain** = building blocks (`create_agent`, `init_chat_model`; AgentExecutor đã **legacy**) · **LangGraph** = orchestrator (state machine có **cycle/branch/HITL/checkpoint**) · **Langfuse** = observability (trace/eval/prompt mgmt).
- LangGraph 3 primitive: **State** (TypedDict/Pydantic, reducer `add_messages`) · **Node** (hàm nhận state, trả **partial update**) · **Edge** (normal · **conditional** · entry · conditional entry). Build→Compile→Invoke.
- Advanced: **Checkpointer** (Postgres/Redis persist) · **interrupt()** (HITL) · **streaming**. Multi-agent: **Supervisor · Hierarchical · Swarm**.
- **MCP** (Anthropic) = **Agent ↔ Tool** (vertical). Host / Client / Server. Transport: **stdio** (subprocess, JSON-RPC qua stdin/stdout) & **streamable-HTTP** (POST + **SSE**). Primitives: **Resources · Prompts · Tools · Sampling · Roots**.
- **A2A** (Google) = **Agent ↔ Agent** (horizontal). Objects: **Agent Card** (discover) · **Task** (lifecycle: submitted/working/input-required/completed) · **Message** · **Artifact** · **Parts**.
- **MCP = vertical capability, A2A = horizontal collaboration** → cùng nhau tạo hệ Agentic AI hoàn chỉnh.

## ⚠️ CẶP DỄ NHẦM
- Retrieval-based (chọn sẵn) ≠ Generative (sinh mới) · Fine-tuning (1 task, model nhỏ) ≠ Instruction-tuning (đa task, model lớn).
- Bi-encoder (retrieve, nhanh) ≠ Cross-encoder (rerank, chính xác) · BM25 (sparse) ≠ dense embedding.
- Multi-Query (không rerank) ≠ RAG-Fusion (có rerank) · Step-back (khái quát hoá) ≠ HyDE (sinh answer giả).
- GraphRAG (có hierarchical + global) ≠ LightRAG (bỏ hierarchical, dual-level) · Local search ≠ Global search (QFS/map-reduce).
- MCP (agent–tool) ≠ A2A (agent–agent) · Function calling (LLM chọn tool, tự implement) ≠ MCP (chuẩn hoá, tái sử dụng).
- domain.yml (không train) ≠ nlu.yml (train) · MemoizationPolicy (story) ≠ TEDPolicy (deep learning) ≠ RulePolicy (rule).
