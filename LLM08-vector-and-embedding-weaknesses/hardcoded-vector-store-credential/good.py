"""
Mitigated equivalents for hardcoded-vector-store-credential.

Every credential below is loaded from the environment (in a real deployment,
typically injected by a secret manager / vault) instead of being a literal
string in source.
"""
import os

import psycopg2
import weaviate
from pinecone import Pinecone
from pymilvus import Collection, connections
from qdrant_client import QdrantClient

# --- Pinecone -----------------------------------------------------------------
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index("prod-knowledge-base")


def upsert_embedding(vector_id: str, embedding: list[float]) -> None:
    index.upsert(vectors=[(vector_id, embedding)])


# --- Weaviate -------------------------------------------------------------------
weaviate_client = weaviate.Client(
    url="https://my-cluster.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=os.environ["WEAVIATE_API_KEY"]),
)


def get_similar_docs(embedding: list[float], k: int = 10):
    return (
        weaviate_client.query.get("Document", ["text"])
        .with_near_vector({"vector": embedding})
        .with_limit(k)
        .do()
    )


# --- Qdrant ---------------------------------------------------------------------
qdrant_client = QdrantClient(
    url="https://a1b2c3d4-e5f6.us-east-1.aws.cloud.qdrant.io",
    api_key=os.environ["QDRANT_API_KEY"],
)


def search_embeddings(collection: str, embedding: list[float], k: int = 10):
    return qdrant_client.search(collection_name=collection, query_vector=embedding, limit=k)


# --- pgvector -------------------------------------------------------------------
conn = psycopg2.connect(
    host="db.internal.example.com",
    port=5432,
    dbname="vectordb",
    user="app_user",
    password=os.environ["PGVECTOR_PASSWORD"],
    sslmode="require",
)


def nearest_neighbors(embedding: list[float], k: int = 10):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM documents ORDER BY embedding <-> %s::vector LIMIT %s",
            (embedding, k),
        )
        return cur.fetchall()


# --- Milvus ---------------------------------------------------------------------
connections.connect(
    alias="default",
    host="milvus-cluster.example.com",
    port="19530",
    user=os.environ["MILVUS_USER"],
    password=os.environ["MILVUS_PASSWORD"],
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
