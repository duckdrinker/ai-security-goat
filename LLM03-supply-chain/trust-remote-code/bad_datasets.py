"""
bad_datasets.py
Triggers trust-remote-code: loads a dataset from the Hugging Face Hub with
trust_remote_code=True, executing the dataset repo's custom loading script at
load time. A compromised or malicious dataset repo can ship code that runs
immediately in this process/pipeline.
"""
from datasets import load_dataset

ds = load_dataset("user/custom-loader-dataset", trust_remote_code=True)
