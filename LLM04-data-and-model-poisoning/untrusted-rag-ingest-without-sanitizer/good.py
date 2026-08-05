"""Mitigated: untrusted content is sanitized before it is embedded.

HTML/markup is stripped, known prompt-injection phrasing is redacted,
and length is capped — the vector store never receives raw untrusted
text.
"""
import re

from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

INJECTION_PATTERNS = re.compile(
    r"(ignore (all|previous) instructions|system prompt)", re.I
)


def sanitize(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)  # strip HTML/markup
    text = INJECTION_PATTERNS.sub("[redacted]", text)
    return text[:20_000]  # cap length


def ingest_support_docs(url: str):
    loader = WebBaseLoader(url)
    docs = loader.load()
    for doc in docs:
        doc.page_content = sanitize(doc.page_content)
    embeddings = OpenAIEmbeddings()
    store = FAISS.from_documents(docs, embeddings)
    store.save_local("faiss_support_index")
    return store
