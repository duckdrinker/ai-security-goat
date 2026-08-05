"""Scrapes an arbitrary external URL and indexes it directly.

Triggers untrusted-rag-ingest-without-sanitizer: content from an
untrusted web source is embedded and persisted to the vector store with
no sanitization/validation step in between.
"""
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


def ingest_support_docs(url: str):
    loader = WebBaseLoader(url)
    docs = loader.load()
    embeddings = OpenAIEmbeddings()
    # Raw scraped HTML/text goes straight into the vector store.
    store = FAISS.from_documents(docs, embeddings)
    store.save_local("faiss_support_index")
    return store
