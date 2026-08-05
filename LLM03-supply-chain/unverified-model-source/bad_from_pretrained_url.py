"""
bad_from_pretrained_url.py
Triggers unverified-model-source: passes an arbitrary URL to from_pretrained()
instead of a verified Hugging Face Hub repo_id (e.g. "org/model-name"). The
weights and tokenizer config are pulled from an unofficial CDN with no
provenance guarantees.
"""
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_SOURCE = "https://models.example-cdn.net/mystery-chat-model/"

model = AutoModelForCausalLM.from_pretrained(MODEL_SOURCE)
tokenizer = AutoTokenizer.from_pretrained(MODEL_SOURCE)
