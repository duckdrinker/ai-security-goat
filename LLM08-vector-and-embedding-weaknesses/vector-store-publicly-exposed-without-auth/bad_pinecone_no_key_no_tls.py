"""
Triggers vector-store-publicly-exposed-without-auth: a Pinecone pod-based
index is addressed directly by its public host with plain HTTP and no api_key
at all. Anyone who can reach the host on the network can read/write/delete
every vector in the index.
"""
from pinecone.grpc import PineconeGRPC as Pinecone

# host is a public endpoint, scheme is http (no TLS), and no api_key is
# supplied anywhere in the client construction.
pc = Pinecone(api_key="", host="http://203.0.113.44:8080")

index = pc.Index(host="http://203.0.113.44:8080")


def upsert_embedding(vector_id: str, embedding: list[float]) -> None:
    index.upsert(vectors=[(vector_id, embedding)])
