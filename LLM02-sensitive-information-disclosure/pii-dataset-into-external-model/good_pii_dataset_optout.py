"""
Negative context: the dataset carries the same newly-recognized PII terms as
bad_passport_dob_dataset.py (passport/DOB), but the endpoint is opted out of
training (data_sharing_mode=opt_out) -- must not trigger
pii-dataset-into-external-model (xygeni-product-backlog#1147).
"""
from datasets import load_dataset
from langchain_mistralai import ChatMistralAI

ds = load_dataset("enrollees_passport_dob.csv")
llm = ChatMistralAI(model="mistral-large")
endpoint = {"base_url": "https://api.mistral.ai", "data_sharing_mode": "opt_out"}
