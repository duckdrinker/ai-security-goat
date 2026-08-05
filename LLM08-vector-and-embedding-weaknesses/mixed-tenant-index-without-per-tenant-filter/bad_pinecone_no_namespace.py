"""
Triggers mixed-tenant-index-without-per-tenant-filter: a single shared
Pinecone index stores embeddings for every tenant, but the query is issued
with no `namespace` and no metadata `filter` restricting results to the
caller's tenant — any tenant's RAG query can retrieve any other tenant's
chunks.
"""
from pinecone import Pinecone

pc = Pinecone(api_key="pc-key")
index = pc.Index("shared-knowledge-base")


def retrieve_context(tenant_id: str, embedding: list[float], top_k: int = 10):
    # tenant_id is accepted as an argument but never used to scope the query.
    return index.query(vector=embedding, top_k=top_k, include_metadata=True)
