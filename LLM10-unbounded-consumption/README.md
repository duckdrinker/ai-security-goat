# LLM10 — Unbounded Consumption

Fixtures for OWASP LLM10:2025 (Unbounded Consumption): code paths that call an LLM, run an agent loop, or query a vector store without any explicit ceiling on cost, time, or resource usage — no token cap, no request timeout, no iteration limit, no top-k limit, and no rate-limiting/circuit-breaker wrapped around any of it. Left unchecked, a single request (or a stuck/adversarial model) can turn into unbounded spend ("denial of wallet"), unbounded latency, or a de facto denial of service.

| Detector | Status | What it flags |
|---|---|---|
| [`inference-call-without-timeout-or-token-cap`](./inference-call-without-timeout-or-token-cap/) | **Confirmed** implemented (observed producing real findings) | An LLM inference call with no max-tokens cap, no request timeout, and no rate-limit/circuit-breaker around it. |
| [`agent-loop-without-iteration-cap`](./agent-loop-without-iteration-cap/) | Not confirmed | An agent loop (manual ReAct, LangGraph, LangChain `AgentExecutor`, recursive agent step, model-decides-when-to-stop, …) with no maximum-iteration/maximum-step cap, relying only on the model itself to decide when to stop. |
| [`vector-search-without-top-k-cap`](./vector-search-without-top-k-cap/) | Not confirmed | A vector store query (Pinecone, Weaviate, Qdrant, Chroma, FAISS, …) with no `top_k`/`limit`/`n_results` cap, or one set so high it caps nothing in practice. |

See each detector's `expected.yaml` for the exact findings a scan of that folder is expected to produce.
