"""
Mitigated: same untrusted-dataset-to-pickle shape as bad_dataset_to_pickle.py,
but the tainted value passes through yaml.safe_load() (a sankxy-recognized
sanitizer) before reaching pickle.loads() -- the sanitizer breaks the taint,
no finding.
"""
import pickle
import yaml
from datasets import load_dataset

ds = load_dataset("attacker/poison-ds")

for row in ds:
    sanitized = yaml.safe_load(row["pickle_data_as_yaml"])
    obj = pickle.loads(sanitized)
    obj.train()
