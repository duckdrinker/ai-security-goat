"""
Control positive: dataset explicitly tagged with a "classification: pii" comment
-- already recognized by the old bespoke PII_HINT regex. Must keep triggering
pii-dataset-into-external-model after the harmonization refactor
(xygeni-product-backlog#1147) -- no regression allowed.
"""
from datasets import load_dataset
from langchain_mistralai import ChatMistralAI

ds = load_dataset("customers.csv")  # classification: pii
llm = ChatMistralAI(model="mistral-large")
endpoint = {"base_url": "https://api.mistral.ai", "data_sharing_mode": "train_on_prompts"}
