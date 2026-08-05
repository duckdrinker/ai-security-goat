"""Local embedding pipeline uses one model to index, another to query.

Triggers embedding-model-mismatch: documents are encoded with
all-MiniLM-L6-v2 at index time but queries are encoded with
all-mpnet-base-v2 at query time — different model, different vector
space, silently wrong nearest neighbors.
"""
import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.Client()
collection = client.create_collection("kb")
index_model = SentenceTransformer("all-MiniLM-L6-v2")
query_model = SentenceTransformer("all-mpnet-base-v2")


def index_documents(ids, texts):
    vectors = index_model.encode(texts).tolist()
    collection.add(ids=ids, embeddings=vectors, documents=texts)


def search(question: str):
    vector = query_model.encode([question]).tolist()
    return collection.query(query_embeddings=vector, n_results=5)
