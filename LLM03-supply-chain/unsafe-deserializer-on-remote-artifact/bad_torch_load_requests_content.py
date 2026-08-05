"""
bad_torch_load_requests_content.py
Triggers unsafe-deserializer-on-remote-artifact: downloads a checkpoint over
HTTP and feeds the raw bytes straight into torch.load() without
weights_only=True. torch.load() uses pickle under the hood, so a malicious
checkpoint can execute arbitrary code on load via a crafted __reduce__.
"""
import io

import requests
import torch

resp = requests.get("https://example-model-bucket.s3.amazonaws.com/ckpt/model.pt", timeout=30)
model = torch.load(io.BytesIO(resp.content))  # no weights_only=True, no integrity check
