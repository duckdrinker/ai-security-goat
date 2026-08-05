"""Indexes via an Azure OpenAI deployment, queries via the direct OpenAI API.

Triggers embedding-model-mismatch: even with "the same" model name,
an Azure-hosted embedding deployment and the direct OpenAI-hosted model
are not guaranteed to produce identical vectors, so retrieval quality
silently degrades in a way that is hard to notice from the code alone.
"""
from openai import AzureOpenAI, OpenAI

azure_client = AzureOpenAI(
    azure_endpoint="https://contoso.openai.azure.com",
    api_key="azure-key",
    api_version="2024-02-01",
)
openai_client = OpenAI()


def index_document(doc_id: str, text: str, collection):
    emb = azure_client.embeddings.create(
        model="text-embedding-3-small", input=text
    ).data[0].embedding
    collection.insert([{"id": doc_id, "vector": emb}])


def query(text: str, collection):
    emb = openai_client.embeddings.create(
        model="text-embedding-3-small", input=text
    ).data[0].embedding
    return collection.search(data=[emb], anns_field="vector", limit=5)
