"""
Triggers vector-store-publicly-exposed-without-auth: connects to a Milvus
instance on a public IP with secure=False (plaintext gRPC channel) and
without user/password, relying purely on network reachability as the only
access control.
"""
from pymilvus import Collection, connections

connections.connect(
    alias="default",
    host="198.51.100.20",
    port="19530",
    secure=False,
    # user / password intentionally not supplied
)

collection = Collection("product_embeddings")


def search(embedding: list[float], k: int = 10):
    return collection.search(
        data=[embedding],
        anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=k,
    )
