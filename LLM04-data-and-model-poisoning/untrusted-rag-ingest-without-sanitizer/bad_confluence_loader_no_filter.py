"""Pulls every page from an external Confluence space and indexes it
verbatim.

Triggers untrusted-rag-ingest-without-sanitizer: any editor of that
external space (and its attachments) can inject content that ends up
as ground truth in the RAG index, with no review or sanitization step.
"""
from langchain_community.document_loaders import ConfluenceLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant


def ingest_external_confluence(space_key: str, url: str, token: str):
    loader = ConfluenceLoader(url=url, token=token)
    docs = loader.load(space_key=space_key, include_attachments=True)
    embeddings = OpenAIEmbeddings()
    return Qdrant.from_documents(
        docs, embeddings, url="http://localhost:6333", collection_name="kb"
    )
