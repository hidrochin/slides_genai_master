# Trắc nghiệm F — Agent, LangGraph & MCP/A2A

> Lý thuyết: [on_tap/F-agent-mcp](../on_tap/F-agent-mcp.md). Đáp án cuối file.

---

**1.** Bốn thành phần điển hình của một AI Agent:
A. Reasoner, Tools, Memory, Planner
B. Encoder, Decoder, Attention, FFN
C. Retriever, Ranker, Generator, Indexer
D. Host, Client, Server, Transport

**2.** Pattern agent mặc định, xen kẽ Thought → Action → Observation:
A. Plan-and-Execute  B. ReAct  C. Reflexion  D. Tree of Thoughts

**3.** Pattern lập kế hoạch đầy đủ trước rồi thực thi tuần tự (ít lãng phí LLM call):
A. ReAct  B. Plan-and-Execute  C. Reflexion  D. Swarm

**4.** Pattern thêm vòng tự phê bình (self-critique) để học từ lỗi lặp lại:
A. ReAct  B. Reflexion  C. Plan-and-Execute  D. ReWOO

**5.** Vai trò của LangGraph trong bộ ba là:
A. Building blocks  B. Orchestrator (state machine)  C. Observability  D. Vector store

**6.** Langfuse dùng để:
A. Ráp agent
B. Cung cấp linh kiện
C. Quan sát (tracing/eval/prompt mgmt/metrics)
D. Lưu trữ vector

**7.** API thay thế `AgentExecutor` (đã legacy) trong LangChain v1.0:
A. create_agent()  B. RunnableChain()  C. LLMChain()  D. AgentLoop()

**8.** Ba primitive của LangGraph:
A. State, Node, Edge
B. Input, Process, Output
C. Prompt, Tool, Memory
D. Map, Reduce, Filter

**9.** Node trong LangGraph trả về:
A. Toàn bộ state mới
B. Partial state update (dict), không mutate trực tiếp
C. Một chuỗi text
D. Không trả về gì

**10.** Reducer `Annotated[list, add_messages]` dùng để:
A. Ghi đè list
B. Append (tích luỹ) thay vì ghi đè
C. Xoá list
D. Sắp xếp list

**11.** Loại edge gọi hàm routing đọc state để chọn node kế tiếp:
A. Normal edge  B. Conditional edge  C. Entry point  D. START edge

**12.** Tính năng LangGraph cho phép dừng giữa graph chờ người duyệt:
A. checkpointer  B. interrupt()  C. astream  D. compile()

**13.** Checkpointer trong LangGraph dùng để:
A. Persist state (Postgres/Redis) → resume sau crash, time-travel
B. Stream token
C. Route edge
D. Validate graph

**14.** Multi-agent pattern trong đó các agent hand-off trực tiếp cho nhau, không có điều phối trung tâm:
A. Supervisor  B. Hierarchical  C. Swarm  D. Pipeline

**15.** MCP (Model Context Protocol) do ai giới thiệu và kết nối gì?
A. Google, agent↔agent
B. Anthropic, agent↔tool/data
C. OpenAI, agent↔user
D. Meta, agent↔model

**16.** Trong kiến trúc MCP, thành phần expose tools/resources/prompts:
A. Host  B. Client  C. Server  D. Transport

**17.** Transport MCP khởi động server như subprocess, giao tiếp qua stdin/stdout (JSON-RPC):
A. streamable-HTTP  B. stdio  C. WebSocket  D. gRPC

**18.** Trong streamable-HTTP, server gửi phản hồi về client qua:
A. HTTP POST  B. Server-Sent Events (SSE)  C. FTP  D. stdin

**19.** MCP primitive cho phép server yêu cầu LLM qua client (giữ privacy + human-in-the-loop):
A. Resources  B. Prompts  C. Sampling  D. Roots

**20.** MCP primitive định nghĩa "workspace boundary" bằng URI client gợi ý:
A. Roots  B. Tools  C. Resources  D. Sampling

**21.** A2A (Google) — object dùng để **discover** agent:
A. Task  B. Agent Card  C. Artifact  D. Message

**22.** Trong A2A, "kết quả cuối bất biến (immutable)" do remote agent tạo là:
A. Message  B. Task  C. Artifact  D. Part

**23.** Vòng đời (lifecycle) của một Task trong A2A KHÔNG bao gồm:
A. submitted  B. working  C. input-required  D. quantized

**24.** Phát biểu ĐÚNG về MCP vs A2A:
A. MCP = vertical (agent–tool), A2A = horizontal (agent–agent)
B. MCP = agent–agent, A2A = agent–tool
C. Cả hai đều do Google phát triển
D. A2A thay thế hoàn toàn MCP

**25.** So với Function Calling, MCP có ưu điểm:
A. Viết tool 1 lần, mọi app/agent tái sử dụng; an toàn hơn (LLM ≠ execute tool)
B. Nhúng cứng tool vào từng app
C. Không cần server
D. Chỉ chạy local

---
### Đáp án
1-A · 2-B · 3-B · 4-B · 5-B · 6-C · 7-A · 8-A · 9-B · 10-B · 11-B · 12-B · 13-A · 14-C · 15-B · 16-C · 17-B · 18-B · 19-C · 20-A · 21-B · 22-C · 23-D · 24-A · 25-A
