# LLM04: Data and Model Poisoning

This category covers ways the data an LLM system learns from, retrieves, or carries forward across turns can be corrupted or exposed: ingesting untrusted content into a RAG index without sanitizing it first, training/fine-tuning on a dataset with no verifiable integrity record, mixing embedding models between indexing and querying, replaying persisted agent memory (including injected content) without revalidation, letting agent memory grow without any bound, and leaving the agent's memory/vector store reachable with no authentication. Each subfolder below is a self-contained, scannable fixture set for one detector.

**Note on detector coverage:** none of the detectors in this category are confirmed implemented in the Xygeni AI Security scanner as of 2026-07-21. Each `expected.yaml` documents the intended behavior per spec — scanning today may produce no finding, which is useful signal about what's not implemented yet rather than a fixture bug.

| Detector | What it flags |
| --- | --- |
| [`untrusted-rag-ingest-without-sanitizer`](untrusted-rag-ingest-without-sanitizer/) | A RAG ingestion pipeline indexes content from an untrusted source (web scraping, user uploads, external wiki spaces) with no sanitization step before it's embedded and stored. |
| [`training-dataset-without-integrity-record`](training-dataset-without-integrity-record/) | A training/fine-tuning dataset is loaded from disk, a URL, a Hub, S3, or an upload with no checksum/hash verified against a known-good record. |
| [`embedding-model-mismatch`](embedding-model-mismatch/) | The embedding model/provider used to index content differs from the one used to query it, producing inconsistent similarity results over the same vector store. |
| [`persistent-context-injection`](persistent-context-injection/) | Agent memory persisted from a previous session is reloaded and reinjected into the live context with no revalidation or sanitization. |
| [`unbounded-agent-memory`](unbounded-agent-memory/) | Agent/conversation memory has no limit on size, turns, or tokens, so it grows without bound over a long-running session. |
| [`agent-memory-store-without-auth`](agent-memory-store-without-auth/) | The backing store for agent memory (vector DB, Redis, Postgres, Mongo, etc.) is reachable with no authentication configured. |
