"""
good_from_pretrained_official.py
Mitigated: loads the model via its official, verified Hugging Face Hub
repo_id, with a pinned revision (commit SHA) so the exact artifact fetched
is reproducible and auditable.
"""
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "meta-llama/Llama-3-8B"
REVISION = "8c22764a7e3675c50d4c7c9a4edb474456022b16"  # pinned commit SHA

model = AutoModelForCausalLM.from_pretrained(MODEL_ID, revision=REVISION)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION)
