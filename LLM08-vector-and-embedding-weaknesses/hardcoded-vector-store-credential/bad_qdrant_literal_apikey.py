"""
Triggers hardcoded-vector-store-credential: QdrantClient is constructed with
its Qdrant Cloud api_key hardcoded as a literal string, instead of pulled
from an environment variable or secret manager.
"""
from qdrant_client import QdrantClient

client = QdrantClient(
    url="https://a1b2c3d4-e5f6.us-east-1.aws.cloud.qdrant.io",
    api_key="qd_9fRt2Km7XpLzV4nWjHc1QsYb8DoAeGtU",
)


def search_embeddings(collection: str, embedding: list[float], k: int = 10):
    return client.search(collection_name=collection, query_vector=embedding, limit=k)
