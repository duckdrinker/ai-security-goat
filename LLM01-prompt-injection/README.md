# LLM01: Prompt Injection

OWASP LLM Top 10:2025 category LLM01 covers inputs that manipulate an LLM's behavior against the intentions of its operator, whether crafted directly by an end user (jailbreaks, obfuscated payloads, unbounded content splicing) or smuggled in indirectly through content the LLM consumes as part of its context — web pages, retrieved documents, emails, images, audio, or search results. The fixtures below each isolate one way a real integration can leave a prompt-injection door open, and the mitigated `good.py` in each folder shows the corresponding fix.

| Detector folder | Description |
|---|---|
| [`obfuscation-keyword-in-prompt`](./obfuscation-keyword-in-prompt/) | Confirmed. Flags obfuscated content (base64, hex, unicode zero-width chars, ROT13, homoglyphs) embedded in a prompt string, designed to evade keyword/content-moderation filters. |
| [`prompt-pinned-to-mutable-label`](./prompt-pinned-to-mutable-label/) | Confirmed. Flags production prompts fetched from an external registry (e.g. Langfuse, LangChain Hub, PromptLayer) by a mutable label/tag (`production`, `latest`, `prod`) instead of an immutable version or hash. |
| [`unbounded-user-content-in-system-prompt`](./unbounded-user-content-in-system-prompt/) | Confirmed. Flags user-controlled content spliced into a system prompt (f-string, concatenation, `.format()`, template rendering) with no length cap or sanitization. |
| [`indirect-injection-sink-without-guardrail`](./indirect-injection-sink-without-guardrail/) | Unconfirmed implementation. Flags agent tools (browsing, RAG retrieval, email reading, web search) that pass externally-sourced content straight into the LLM context with no sanitization guardrail. |
| [`multimodal-input-without-sanitization`](./multimodal-input-without-sanitization/) | Unconfirmed implementation. Flags multimodal input (images, audio, video, screenshots) passed directly to a model with no content-safety check beforehand. |
| [`agent-tool-without-input-guardrail`](./agent-tool-without-input-guardrail/) | Unconfirmed implementation. Flags side-effect agent tools (shell exec, SQL, email send, file delete, funds transfer) invoked with an LLM-generated argument that is never validated before execution. |

See the confirmation status note in each `expected.yaml` — the first three detectors have been validated against the detection engine's unit tests; the last three document intended behavior per spec and may not yet produce findings.
