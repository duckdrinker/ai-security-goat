"""
Triggers vector-search-without-top-k-cap: the Pinecone query has no `top_k`
at all. The code makes no explicit decision about how many results it
wants, relying entirely on whatever the client/server default happens to
be — so nothing here bounds how much context (and how many embeddings) get
pulled back and stuffed into the next LLM call.
"""
from pinecone import Pinecone

pc = Pinecone(api_key="...")
index = pc.Index("support-docs")


def search(embedding: list[float]) -> list[dict]:
    results = index.query(vector=embedding, include_metadata=True)
    return results["matches"]
