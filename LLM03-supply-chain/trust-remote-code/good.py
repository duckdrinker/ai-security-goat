"""
Mitigated: no custom remote code is executed. transformers/sentence-transformers
loads explicitly set trust_remote_code=False; the datasets/diffusers loads omit
the flag entirely, which defaults to False.
"""
from transformers import AutoModel
from sentence_transformers import SentenceTransformer
from datasets import load_dataset
from diffusers import DiffusionPipeline

model = AutoModel.from_pretrained("bert-base-uncased", trust_remote_code=False)
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", trust_remote_code=False)
ds = load_dataset("squad")
pipe = DiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
