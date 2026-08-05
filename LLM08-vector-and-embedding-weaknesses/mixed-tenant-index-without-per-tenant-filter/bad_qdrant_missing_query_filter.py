"""
Triggers mixed-tenant-index-without-per-tenant-filter: all tenants' vectors
live in the single "support_tickets" Qdrant collection, distinguished only by
a "tenant_id" payload field. search() is called without a `query_filter`, so
Qdrant scores and returns nearest neighbours across every tenant's data.
"""
from qdrant_client import QdrantClient

client = QdrantClient(url="https://my-cluster.cloud.qdrant.io", api_key="qdrant-key")


def search_tickets(tenant_id: str, embedding: list[float], k: int = 10):
    return client.search(
        collection_name="support_tickets",
        query_vector=embedding,
        limit=k,
        # No query_filter=Filter(must=[FieldCondition(key="tenant_id", ...)])
    )
