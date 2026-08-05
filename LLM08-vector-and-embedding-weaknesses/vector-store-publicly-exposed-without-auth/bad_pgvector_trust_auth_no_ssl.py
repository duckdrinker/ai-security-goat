"""
Triggers vector-store-publicly-exposed-without-auth: connects to a
pgvector-backed Postgres instance on a public host with sslmode=disable and
no password, relying on pg_hba.conf "trust" auth. Anyone on the network can
open a session and run vector similarity queries or dump the whole table.
"""
import psycopg2

conn = psycopg2.connect(
    host="203.0.113.77",
    port=5432,
    dbname="vectordb",
    user="postgres",
    password="",
    sslmode="disable",
)


def nearest_neighbors(embedding: list[float], k: int = 10):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, content FROM documents ORDER BY embedding <-> %s::vector LIMIT %s",
            (embedding, k),
        )
        return cur.fetchall()
