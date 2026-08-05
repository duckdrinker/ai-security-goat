"""
Mitigated equivalents for vector-store-publicly-exposed-without-auth.

Each connection below requires an API key / credential (loaded from the
environment, never hardcoded) AND uses TLS, so traffic is both authenticated
and encrypted in transit.
"""
import os

import psycopg2
import weaviate
from pinecone.grpc import PineconeGRPC as Pinecone
from pymilvus import Collection, connections
from qdrant_client import QdrantClient

# --- Pinecone: managed HTTPS endpoint + API key -----------------------------
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index = pc.Index(host="https://my-index-abc123.svc.us-east1-aws.pinecone.io")


def upsert_embedding(vector_id: str, embedding: list[float]) -> None:
    index.upsert(vectors=[(vector_id, embedding)])


# --- Weaviate: HTTPS + API key auth -----------------------------------------
weaviate_client = weaviate.Client(
    url="https://my-cluster.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key=os.environ["WEAVIATE_API_KEY"]),
)


def get_similar_docs(embedding: list[float], k: int = 10):
    return (
        weaviate_client.query.get("Document", ["text", "source"])
        .with_near_vector({"vector": embedding})
        .with_limit(k)
        .do()
    )


# --- Qdrant: TLS + API key ---------------------------------------------------
qdrant_client = QdrantClient(
    url="https://my-cluster.cloud.qdrant.io",
    https=True,
    api_key=os.environ["QDRANT_API_KEY"],
)


def search_embeddings(collection: str, embedding: list[float], k: int = 10):
    return qdrant_client.search(collection_name=collection, query_vector=embedding, limit=k)


# --- Milvus: secure channel + credentials -----------------------------------
connections.connect(
    alias="default",
    host="my-milvus-cluster.example.com",
    port="19530",
    secure=True,
    user=os.environ["MILVUS_USER"],
    password=os.environ["MILVUS_PASSWORD"],
)
collection = Collection("product_embeddings")


def search(embedding: list[float], k: int = 10):
    return collection.search(
        data=[embedding],
        anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=k,
    )


# --- pgvector: TLS-enforced connection, real credentials --------------------
conn = psycopg2.connect(
    host="my-postgres-cluster.example.com",
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
