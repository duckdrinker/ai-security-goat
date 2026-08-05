"""
Triggers hardcoded-vector-store-credential: the Postgres/pgvector password is
a literal string embedded directly in the connection call, rather than
sourced from the environment or a secrets manager.
"""
import psycopg2

conn = psycopg2.connect(
    host="db.internal.example.com",
    port=5432,
    dbname="vectordb",
    user="app_user",
    password="Tr0ub4dor&3-VectorDB!",
    sslmode="require",
)


def nearest_neighbors(embedding: list[float], k: int = 10):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM documents ORDER BY embedding <-> %s::vector LIMIT %s",
            (embedding, k),
        )
        return cur.fetchall()
