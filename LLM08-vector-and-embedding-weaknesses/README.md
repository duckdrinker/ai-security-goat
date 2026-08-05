# LLM08 — Vector and Embedding Weaknesses

Covers OWASP LLM Top 10:2025 category **LLM08:2025**: risks specific to how
Retrieval-Augmented Generation (RAG) pipelines store and query vector
embeddings — vector stores left reachable without authentication or
encryption, multi-tenant indexes that don't scope queries to the calling
tenant (allowing cross-tenant data leakage through similarity search), and
vector store credentials hardcoded directly in source instead of loaded from
environment/secret storage.

| Detector | What it flags |
|---|---|
| [`vector-store-publicly-exposed-without-auth`](vector-store-publicly-exposed-without-auth/) | A vector store client/config (Pinecone, Weaviate, Qdrant, Milvus, pgvector) connects to a public host or open binding with no API key and no TLS, exposing the index to any network peer. |
| [`mixed-tenant-index-without-per-tenant-filter`](mixed-tenant-index-without-per-tenant-filter/) | A similarity query against a multi-tenant index/collection has no per-tenant scoping (namespace, metadata filter, or `WHERE tenant_id = ...`), risking cross-tenant data leakage. |
| [`hardcoded-vector-store-credential`](hardcoded-vector-store-credential/) | A vector store API key, password, or token is hardcoded as a literal string in source instead of being loaded from the environment or a secret manager. |
