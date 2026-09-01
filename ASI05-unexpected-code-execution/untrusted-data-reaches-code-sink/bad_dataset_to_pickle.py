"""
bad_dataset_to_pickle.py
Triggers untrusted-data-reaches-code-sink: an untrusted Hugging Face dataset
(AI-specific source) is iterated and its rows are deserialized with
pickle.loads() in the same file -- a single chained Critical finding, not two
isolated ones.
"""
import pickle
from datasets import load_dataset

ds = load_dataset("attacker/poison-ds")

for row in ds:
    malicious_bytes = row["pickle_data"]
    obj = pickle.loads(malicious_bytes)
    obj.train()
