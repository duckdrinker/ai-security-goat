"""
Triggers mixed-tenant-index-without-per-tenant-filter: the "Document" class
holds chunks from all customers in one Weaviate collection. The near-vector
search has no `.with_where(...)` clause on tenant_id, so the nearest
neighbours returned can belong to any customer, not just the caller's.
"""
import weaviate

client = weaviate.Client(url="https://my-cluster.weaviate.network")


def search_customer_docs(customer_id: str, embedding: list[float], k: int = 10):
    # customer_id is never wired into a where-filter.
    return (
        client.query.get("Document", ["text", "customer_id"])
        .with_near_vector({"vector": embedding})
        .with_limit(k)
        .do()
    )
