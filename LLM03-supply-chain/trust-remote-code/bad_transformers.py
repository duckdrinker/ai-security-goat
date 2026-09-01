"""
bad_transformers.py
Triggers trust-remote-code: loads a model from the Hugging Face Hub with
trust_remote_code=True, which executes arbitrary custom modeling code shipped
inside the model repo at load time. A compromised or malicious repo owner can
ship code that runs immediately in this process/pipeline.
"""
from transformers import AutoModel, AutoTokenizer

model = AutoModel.from_pretrained("user/custom-arch-model", trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained("user/custom-arch-model", trust_remote_code=True)
