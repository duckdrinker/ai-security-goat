"""
Triggers vector-store-publicly-exposed-without-auth: the Weaviate client
connects over plain HTTP (no TLS) to a host bound on all interfaces, with
auth_client_secret left unset — anonymous access is accepted by the server
and traffic (including embeddings and payloads) is sent unencrypted.
"""
import weaviate

client = weaviate.Client(
    url="http://0.0.0.0:8080",
    # No auth_client_secret => anonymous access, no bearer/API key required.
)


def get_similar_docs(embedding: list[float], k: int = 10):
    return (
        client.query.get("Document", ["text", "source"])
        .with_near_vector({"vector": embedding})
        .with_limit(k)
        .do()
    )
