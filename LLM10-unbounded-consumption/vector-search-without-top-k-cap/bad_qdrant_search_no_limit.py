"""
Triggers vector-search-without-top-k-cap: `limit` is set to one million,
which for this collection is equivalent to "return the whole index". The
parameter exists and is even set explicitly, but it does not function as a
cap — it defeats the purpose of top-k retrieval and lets a single query
pull back and process the entire vector store.
"""
from qdrant_client import QdrantClient

client = QdrantClient(url="http://qdrant.internal:6333")


def search(collection: str, embedding: list[float]) -> list[dict]:
    hits = client.search(
        collection_name=collection,
        query_vector=embedding,
        limit=1_000_000,
    )
    return [hit.payload for hit in hits]
