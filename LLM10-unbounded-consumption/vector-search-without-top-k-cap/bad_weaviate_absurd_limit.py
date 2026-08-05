"""
Triggers vector-search-without-top-k-cap: the limit is technically present
but set to 100,000 — several orders of magnitude beyond anything a RAG
pipeline needs per query. In practice this is no cap at all: any collection
smaller than that returns everything it has, and a large one can still
return a huge result set that gets serialized and fed downstream.
"""
import weaviate

client = weaviate.connect_to_local()


def search(query_vector: list[float]) -> list[dict]:
    response = client.collections.get("SupportDocs").query.near_vector(
        near_vector=query_vector,
        limit=100_000,
    )
    return [obj.properties for obj in response.objects]
