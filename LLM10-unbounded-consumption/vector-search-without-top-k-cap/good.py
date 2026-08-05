"""
Mitigated equivalent: an explicit, small, application-chosen `top_k` that
is decoupled from index size and from whatever the client/server default
might be. The same discipline applies to any vector store — Weaviate's
`limit`, Qdrant's `limit`, Chroma's `n_results`, FAISS's `k` — always pass a
fixed, reviewed value instead of relying on defaults or index size. Does
not trigger vector-search-without-top-k-cap.
"""
from pinecone import Pinecone

pc = Pinecone(api_key="...")
index = pc.Index("support-docs")

TOP_K = 10


def search(embedding: list[float]) -> list[dict]:
    results = index.query(vector=embedding, top_k=TOP_K, include_metadata=True)
    return results["matches"]
