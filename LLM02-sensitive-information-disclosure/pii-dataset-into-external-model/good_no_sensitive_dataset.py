"""
Negative control: no sensitive term anywhere (filename, comments, or code) --
must not trigger pii-dataset-into-external-model. Guards against false positives
introduced by widening the shared sensitivity vocabulary
(xygeni-product-backlog#1147).
"""
from datasets import load_dataset
from langchain_mistralai import ChatMistralAI

ds = load_dataset("sales_2025.csv")
llm = ChatMistralAI(model="mistral-large")
endpoint = {"base_url": "https://api.mistral.ai", "data_sharing_mode": "train_on_prompts"}
