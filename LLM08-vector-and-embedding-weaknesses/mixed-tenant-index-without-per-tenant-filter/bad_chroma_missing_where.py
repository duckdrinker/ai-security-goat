"""
Triggers mixed-tenant-index-without-per-tenant-filter: a single Chroma
collection is shared by every workspace, but query() is called without a
`where={"workspace_id": ...}` filter, so results are drawn from all
workspaces' embeddings indiscriminately.
"""
import chromadb

client = chromadb.HttpClient(host="chroma.internal", port=8000)
collection = client.get_collection("shared_workspace_docs")


def query_workspace(workspace_id: str, embedding: list[float], n_results: int = 10):
    return collection.query(query_embeddings=[embedding], n_results=n_results)
