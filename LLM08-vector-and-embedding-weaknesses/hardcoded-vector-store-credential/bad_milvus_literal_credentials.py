"""
Triggers hardcoded-vector-store-credential: Milvus connection credentials
(user + password) are literal strings in the source, instead of being read
from configuration or a secret store.
"""
from pymilvus import Collection, connections

connections.connect(
    alias="default",
    host="milvus-cluster.example.com",
    port="19530",
    user="root",
    password="Milvus2024!Prod",
    secure=True,
)

collection = Collection("product_embeddings")


def search(embedding: list[float], k: int = 10):
    return collection.search(
        data=[embedding],
        anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=k,
    )
