"""
Triggers vector-store-publicly-exposed-without-auth: QdrantClient is pointed
at host="0.0.0.0" (i.e. the server was started bound to all interfaces and is
addressed as such) with https=False and api_key omitted. Any network peer
that can route to the box gets full read/write access to every collection.
"""
from qdrant_client import QdrantClient

client = QdrantClient(
    host="0.0.0.0",
    port=6333,
    https=False,
    # api_key intentionally omitted
)


def search_embeddings(collection: str, embedding: list[float], k: int = 10):
    return client.search(collection_name=collection, query_vector=embedding, limit=k)
