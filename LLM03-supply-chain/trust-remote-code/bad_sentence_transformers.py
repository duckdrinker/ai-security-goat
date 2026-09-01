"""
bad_sentence_transformers.py
Triggers trust-remote-code: loads a sentence-transformers embedding model with
trust_remote_code=True, executing the repo's custom modules.json-referenced
code at load time. A compromised or malicious repo owner can ship code that
runs immediately in this process/pipeline.
"""
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("user/custom-embedding-model", trust_remote_code=True)
