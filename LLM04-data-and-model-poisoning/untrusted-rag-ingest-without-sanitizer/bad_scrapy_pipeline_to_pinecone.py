"""Scrapy pipeline pushes scraped web pages straight into Pinecone.

Triggers untrusted-rag-ingest-without-sanitizer: fully untrusted
crawled content is embedded and upserted into a production vector
index on every crawl, with no cleaning/filtering stage in the
pipeline.
"""
from openai import OpenAI
from pinecone import Pinecone

client = OpenAI()
pc = Pinecone(api_key="pc-api-key")
index = pc.Index("web-kb")


class IndexPipeline:
    def process_item(self, item, spider):
        text = item["body"]  # raw scraped HTML text, no cleaning
        emb = client.embeddings.create(
            model="text-embedding-3-small", input=text
        ).data[0].embedding
        index.upsert([(item["url"], emb, {"text": text})])
        return item
