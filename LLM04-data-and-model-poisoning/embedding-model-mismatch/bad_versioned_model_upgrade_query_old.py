"""Index was migrated to a new embedding model, but a legacy query path
still uses the deprecated one.

Triggers embedding-model-mismatch: reindex_kb builds the store with
text-embedding-3-small, but legacy_query still calls the deprecated
text-embedding-ada-002 — after the migration, retrieval silently
compares vectors from two incompatible embedding spaces.
"""
import weaviate
from langchain_community.vectorstores import Weaviate
from langchain_openai import OpenAIEmbeddings

client = weaviate.Client("http://localhost:8080")


def reindex_kb(docs):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Weaviate.from_documents(docs, embeddings, client=client, index_name="KB")


def legacy_query(store, question: str):
    legacy_embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    vector = legacy_embeddings.embed_query(question)
    return store.similarity_search_by_vector(vector)
