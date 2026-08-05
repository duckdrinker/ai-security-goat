"""Mitigated: a single shared embedding model/function is used for both
indexing and querying, guaranteeing vectors live in the same space.
"""
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

EMBEDDING_MODEL = "text-embedding-3-small"


def get_embeddings():
    return OpenAIEmbeddings(model=EMBEDDING_MODEL)


def index_documents(docs):
    return FAISS.from_documents(docs, get_embeddings())


def query_index(store, question: str):
    # Uses the store's own embedding function — same model as indexing.
    return store.similarity_search(question, k=5)
