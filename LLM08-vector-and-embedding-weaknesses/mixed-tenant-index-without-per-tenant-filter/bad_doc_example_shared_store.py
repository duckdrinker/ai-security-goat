from acme_vectorstore import VectorStore

store = VectorStore()
store.add(documents=tenant_a_docs, namespace="tenant_a")
store.add(documents=tenant_b_docs, namespace="tenant_b")


def search(query):
    return store.similarity_search(query)
