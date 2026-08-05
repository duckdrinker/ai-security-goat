"""Flask endpoint indexes a user-uploaded PDF immediately.

Triggers untrusted-rag-ingest-without-sanitizer: the extracted text of
an arbitrary user upload is embedded and added to the shared vector
store with no content sanitization/validation before storage.
"""
from flask import Flask, request
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

app = Flask(__name__)
embeddings = OpenAIEmbeddings()
vectordb = Chroma(collection_name="kb", embedding_function=embeddings)


@app.route("/upload", methods=["POST"])
def upload_document():
    file = request.files["file"]
    path = f"/tmp/{file.filename}"
    file.save(path)
    docs = PyPDFLoader(path).load()
    vectordb.add_documents(docs)  # untrusted upload indexed as-is
    return {"status": "indexed"}
