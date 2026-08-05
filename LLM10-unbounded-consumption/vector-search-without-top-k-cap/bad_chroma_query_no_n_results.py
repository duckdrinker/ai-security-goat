"""
Triggers vector-search-without-top-k-cap: Chroma's `query()` accepts
`n_results` specifically to cap how many nearest neighbours come back, and
it is left unset here. The call relies entirely on the client's default,
which is not sized to this collection and is not decoupled from how the
collection grows over time.
"""
import chromadb

client = chromadb.HttpClient(host="chroma.internal", port=8000)
collection = client.get_collection("knowledge-base")


def search(query_embedding: list[float]) -> list[str]:
    results = collection.query(query_embeddings=[query_embedding])
    return results["documents"][0]
