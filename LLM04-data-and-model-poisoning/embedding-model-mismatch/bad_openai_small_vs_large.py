"""Indexes with one OpenAI embedding model, queries with another.

Triggers embedding-model-mismatch: text-embedding-3-small is used to
build the index but text-embedding-3-large is used at query time
against that same index — different dimensionality/semantics make
similarity scores meaningless and the retrieval surface unreliable.
"""
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


def index_documents(docs):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return FAISS.from_documents(docs, embeddings)


def query_index(store, question: str):
    query_embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    return store.similarity_search_by_vector(query_embeddings.embed_query(question))
