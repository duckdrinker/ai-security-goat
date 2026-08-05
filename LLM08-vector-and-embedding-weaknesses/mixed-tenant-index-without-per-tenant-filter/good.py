"""
Mitigated equivalents for mixed-tenant-index-without-per-tenant-filter.

Each query below scopes results to the caller's own tenant, either via the
vector store's native namespace concept or an explicit metadata/WHERE filter
on tenant_id — no cross-tenant leakage.
"""
import chromadb
import psycopg2
import weaviate
from pinecone import Pinecone
from qdrant_client import QdrantClient
from qdrant_client.http.models import FieldCondition, Filter, MatchValue

# --- Pinecone: per-tenant namespace ------------------------------------------
pc = Pinecone(api_key="pc-key")
index = pc.Index("shared-knowledge-base")


def retrieve_context(tenant_id: str, embedding: list[float], top_k: int = 10):
    return index.query(
        vector=embedding, top_k=top_k, include_metadata=True, namespace=tenant_id
    )


# --- Weaviate: where-filter on tenant --------------------------------------
weaviate_client = weaviate.Client(url="https://my-cluster.weaviate.network")


def search_customer_docs(customer_id: str, embedding: list[float], k: int = 10):
    return (
        weaviate_client.query.get("Document", ["text", "customer_id"])
        .with_near_vector({"vector": embedding})
        .with_where(
            {
                "path": ["customer_id"],
                "operator": "Equal",
                "valueText": customer_id,
            }
        )
        .with_limit(k)
        .do()
    )


# --- Qdrant: query_filter on tenant_id payload field ------------------------
qdrant_client = QdrantClient(url="https://my-cluster.cloud.qdrant.io", api_key="qdrant-key")


def search_tickets(tenant_id: str, embedding: list[float], k: int = 10):
    return qdrant_client.search(
        collection_name="support_tickets",
        query_vector=embedding,
        limit=k,
        query_filter=Filter(
            must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))]
        ),
    )


# --- pgvector: WHERE tenant_id = %s ------------------------------------------
conn = psycopg2.connect("postgresql://app_user:pw@db.internal:5432/vectordb")


def nearest_neighbors(tenant_id: str, embedding: list[float], k: int = 10):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM documents WHERE tenant_id = %s "
            "ORDER BY embedding <-> %s::vector LIMIT %s",
            (tenant_id, embedding, k),
        )
        return cur.fetchall()


# --- Chroma: where filter on workspace_id ------------------------------------
chroma_client = chromadb.HttpClient(host="chroma.internal", port=8000)
collection = chroma_client.get_collection("shared_workspace_docs")


def query_workspace(workspace_id: str, embedding: list[float], n_results: int = 10):
    return collection.query(
        query_embeddings=[embedding],
        n_results=n_results,
        where={"workspace_id": workspace_id},
    )
