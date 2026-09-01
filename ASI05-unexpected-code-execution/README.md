# ASI05: Unexpected Code Execution

OWASP Agentic Security Initiative category, not part of the LLM Top 10:2025 taxonomy — added 2026-08-31 (xygeni/xygeni-product-backlog#1357) alongside `ASI03-identity-abuse/` as this collection's second non-LLM category. Covers the taint-flow detector, which connects an untrusted **source** to a dangerous **sink** across the codebase (same file, another file, even another language) instead of flagging each pattern in isolation — turning two fragmented, easy-to-miss findings into one high-confidence chained finding.

| Detector | What it flags |
|---|---|
| [`untrusted-data-reaches-code-sink`](./untrusted-data-reaches-code-sink/) | An untrusted dataset/model source (or, when a matching SAST finding already exists, a generic untrusted source too) flows into a dangerous sink — `pickle.loads`, `eval`/`exec`, `subprocess` with `shell=True`, etc. Supports cross-file and JS/TS chains. |

**Structural note:** unlike every other detector folder in this collection, several fixtures here are inherently **multi-file** (a source in one file, a sink in another; a "confirm-source" case that depends on an existing SAST finding already being present in the same file). `expected.yaml` uses a `files:` (plural) key for those cross-file findings instead of the usual single `file:`.
