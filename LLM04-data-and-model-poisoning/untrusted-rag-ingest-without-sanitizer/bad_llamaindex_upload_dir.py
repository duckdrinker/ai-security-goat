"""Indexes every file a user uploads to a shared folder, unfiltered.

Triggers untrusted-rag-ingest-without-sanitizer: llama-index
SimpleDirectoryReader reads raw user uploads and feeds them straight
into the index, so a malicious upload can poison the knowledge base.
"""
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex


def ingest_user_uploads(upload_dir: str = "/data/uploads"):
    documents = SimpleDirectoryReader(upload_dir).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir="./storage")
    return index
