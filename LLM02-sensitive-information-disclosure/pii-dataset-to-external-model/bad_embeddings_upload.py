"""
Pushes raw customer support transcripts (containing emails and phone numbers)
to OpenAI's embeddings API to build a vector index for semantic search, without
anonymizing the text first. Triggers pii-dataset-to-external-model because the
raw PII-laden text is sent to an external embeddings provider.
"""
import pandas as pd
from openai import OpenAI

client = OpenAI()

tickets = pd.read_csv("data/support_tickets.csv")  # columns: ticket_id, customer_email, customer_phone, transcript


def embed_tickets(df: pd.DataFrame):
    vectors = []
    for _, row in df.iterrows():
        text = f"{row['transcript']} (contact: {row['customer_email']}, {row['customer_phone']})"
        resp = client.embeddings.create(model="text-embedding-3-small", input=text)
        vectors.append((row["ticket_id"], resp.data[0].embedding))
    return vectors


embed_tickets(tickets)
