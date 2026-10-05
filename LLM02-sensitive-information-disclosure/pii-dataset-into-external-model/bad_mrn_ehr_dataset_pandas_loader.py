"""
Same scenario as bad_mrn_ehr_dataset.py (MRN/EHR vocabulary, no opt-out), but
loaded via pandas instead of datasets.load_dataset() -- confirmed (2026-10-05,
xygeni v6.20.0) to be the loader shape the shared-sensitivity classifier actually
recognizes new vocabulary through. Kept as a separate fixture rather than editing
the original, which intentionally stays faithful to the dev's own literal example
(xygeni-product-backlog#1147) to keep documenting the load_dataset() gap.
"""
import pandas as pd
from langchain_mistralai import ChatMistralAI

ds = pd.read_csv("registry_mrn_ehr.csv")
llm = ChatMistralAI(model="mistral-large")
endpoint = {"base_url": "https://api.mistral.ai", "data_sharing_mode": "train_on_prompts"}
