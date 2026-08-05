"""
Mitigated: support ticket text is scrubbed of emails and phone numbers with a
redaction function before being sent to the embeddings API.
"""
import re

import pandas as pd
from openai import OpenAI

client = OpenAI()

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE_RE = re.compile(r"\+?\d[\d\-\s]{7,}\d")


def redact(text: str) -> str:
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = PHONE_RE.sub("[PHONE]", text)
    return text


tickets = pd.read_csv("data/support_tickets.csv")


def embed_tickets(df: pd.DataFrame):
    vectors = []
    for _, row in df.iterrows():
        safe_text = redact(row["transcript"])
        resp = client.embeddings.create(model="text-embedding-3-small", input=safe_text)
        vectors.append((row["ticket_id"], resp.data[0].embedding))
    return vectors


embed_tickets(tickets)
