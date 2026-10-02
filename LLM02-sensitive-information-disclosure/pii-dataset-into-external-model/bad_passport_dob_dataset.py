"""
Loads a dataset whose filename encodes passport/DOB fields -- personal PII terms
from the shared sensitivity catalog that the old bespoke PII_HINT regex did not
recognize -- and feeds it to an external model with no opt-out configured. Should
trigger pii-dataset-into-external-model once PII classification is delegated to the
shared sensitivity classifier (xygeni-product-backlog#1147).
"""
from datasets import load_dataset
from langchain_mistralai import ChatMistralAI

ds = load_dataset("enrollees_passport_dob.csv")
llm = ChatMistralAI(model="mistral-large")
endpoint = {"base_url": "https://api.mistral.ai", "data_sharing_mode": "train_on_prompts"}
