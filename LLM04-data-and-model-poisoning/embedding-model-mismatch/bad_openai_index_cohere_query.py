"""Indexes with OpenAI embeddings, queries with Cohere embeddings.

Triggers embedding-model-mismatch: vectors from two different embedding
providers/spaces are compared directly in the same Pinecone index —
the comparison is meaningless and opens the door to manipulated or
low-confidence retrieval results being trusted.
"""
import cohere
from openai import OpenAI
from pinecone import Pinecone

openai_client = OpenAI()
co = cohere.Client("co-api-key")
pc = Pinecone(api_key="pc-api-key")
index = pc.Index("kb")


def index_document(doc_id: str, text: str):
    emb = openai_client.embeddings.create(
        model="text-embedding-3-small", input=text
    ).data[0].embedding
    index.upsert([(doc_id, emb)])


def query(text: str):
    emb = co.embed(texts=[text], model="embed-english-v3.0").embeddings[0]
    return index.query(vector=emb, top_k=5)
