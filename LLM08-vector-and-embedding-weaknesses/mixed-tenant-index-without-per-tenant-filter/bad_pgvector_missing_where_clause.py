"""
Triggers mixed-tenant-index-without-per-tenant-filter: the "documents" table
in the shared pgvector database stores a tenant_id column, but the nearest-
neighbour query has no `WHERE tenant_id = %s` clause, so the ORDER BY / LIMIT
ranks and returns chunks belonging to every tenant in the table.
"""
import psycopg2

conn = psycopg2.connect("postgresql://app_user:pw@db.internal:5432/vectordb")


def nearest_neighbors(tenant_id: str, embedding: list[float], k: int = 10):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM documents ORDER BY embedding <-> %s::vector LIMIT %s",
            (embedding, k),
        )
        return cur.fetchall()
