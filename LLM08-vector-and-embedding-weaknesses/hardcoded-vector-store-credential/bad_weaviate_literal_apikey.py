"""
Triggers hardcoded-vector-store-credential: the Weaviate API key is passed as
a literal string to AuthApiKey instead of being loaded from configuration/
secret storage.
"""
import weaviate

client = weaviate.Client(
    url="https://my-cluster.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key="wv-l8n2K9pQ7mZxR4vTbYc3eHjD6sFgA1o"),
)


def get_similar_docs(embedding: list[float], k: int = 10):
    return (
        client.query.get("Document", ["text"])
        .with_near_vector({"vector": embedding})
        .with_limit(k)
        .do()
    )
