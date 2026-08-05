# LLM09: Misinformation

This category covers static checks for the **absence of a grounding/citation guardrail** around LLM-generated content — it does not, and cannot, verify whether the content a model actually produces is true. Detecting real-world factual accuracy is not statically computable, so every detector here is a narrow structural check: does the code call an LLM in a way that has no retrieval step feeding it facts, and no instruction (or pipeline component) requiring it to cite sources? A `pass` result only means a grounding/citation mechanism is *present* in the code — it says nothing about whether the mechanism is well-implemented or whether the model's output is correct.

| Detector | High-risk pattern | Mitigation checked for |
|---|---|---|
| [`high-stakes-domain-without-grounding-or-citation`](./high-stakes-domain-without-grounding-or-citation/) | Code that generates content in a high-stakes domain (legal, medical, financial) by calling an LLM directly, with no retrieval step and no instruction to cite sources. | A retrieval/RAG step before generation, and/or an explicit instruction for the model to cite its sources. |
| [`public-agent-missing-factuality-guardrail`](./public-agent-missing-factuality-guardrail/) | A publicly-exposed agent (customer-facing chatbot, public API/channel) with no factuality-verification or citation guardrail configured anywhere in its pipeline. | Any factuality/citation guardrail wired into the pipeline (e.g. a NeMo Guardrails fact-checking rail, a citation-verifier step). |

**Note on detector coverage:** as documented in the parent `ai-security-goat/README.md`, neither detector in this category is confirmed implemented in the Xygeni AI Security scanner as of 2026-07-21. Each `expected.yaml` below states this explicitly — a scan producing no findings here is expected signal, not a fixture bug.
