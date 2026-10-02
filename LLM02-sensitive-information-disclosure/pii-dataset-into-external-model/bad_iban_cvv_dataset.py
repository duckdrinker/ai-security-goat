"""
Loads a dataset whose filename encodes IBAN/CVV fields -- financial PII terms
from the shared sensitivity catalog that the old bespoke PII_HINT regex did not
recognize (it only covered "credit_card") -- and feeds it to an external model
with no opt-out configured (xygeni-product-backlog#1147).
"""
import pandas as pd
from langchain_mistralai import ChatMistralAI

ds = pd.read_parquet("payments_iban_cvv.parquet")
llm = ChatMistralAI(model="mistral-large")
endpoint = {"base_url": "https://api.mistral.ai", "data_sharing_mode": "train_on_prompts"}
