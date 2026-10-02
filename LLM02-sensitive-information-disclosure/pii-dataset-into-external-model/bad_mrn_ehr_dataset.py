"""
Loads a dataset whose filename encodes MRN/EHR fields -- health PII terms from
the shared sensitivity catalog beyond the old bespoke regex's patient|medical|
health_record vocabulary -- and feeds it to an external model with no opt-out
configured (xygeni-product-backlog#1147).
"""
from datasets import load_dataset
from langchain_mistralai import ChatMistralAI

ds = load_dataset("cohort_mrn_ehr.csv")
llm = ChatMistralAI(model="mistral-large")
endpoint = {"base_url": "https://api.mistral.ai", "data_sharing_mode": "train_on_prompts"}
