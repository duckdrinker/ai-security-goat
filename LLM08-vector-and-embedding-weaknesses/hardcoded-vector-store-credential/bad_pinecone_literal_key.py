"""
Triggers hardcoded-vector-store-credential: the Pinecone API key is a literal
string baked into the source file. Anyone with read access to the repo (or a
leaked copy of this file) gets full access to the index.
"""
from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_5x7Kd_9mFqW3aRt8LzN2vJhY6bXcQeT1uPsG4oDwMk")
index = pc.Index("prod-knowledge-base")


def upsert_embedding(vector_id: str, embedding: list[float]) -> None:
    index.upsert(vectors=[(vector_id, embedding)])
