"""
good_torch_load_weights_only.py
Mitigated: downloads the checkpoint, verifies its integrity against a known
hash, and loads it with weights_only=True so torch.load() restricts
unpickling to plain tensors/state-dict data instead of arbitrary objects.
"""
import hashlib
import urllib.request

import torch

CHECKPOINT_URL = "https://cdn.example-model-host.io/checkpoints/finetuned_v3.pt"
LOCAL_PATH = "/tmp/finetuned_v3.pt"
EXPECTED_SHA256 = "a1b2c3d4e5f60718293a4b5c6d7e8f9091a2b3c4d5e6f708192a3b4c5d6e7f8"

urllib.request.urlretrieve(CHECKPOINT_URL, LOCAL_PATH)

with open(LOCAL_PATH, "rb") as f:
    digest = hashlib.sha256(f.read()).hexdigest()
if digest != EXPECTED_SHA256:
    raise ValueError("Checkpoint hash mismatch — refusing to load")

state_dict = torch.load(LOCAL_PATH, weights_only=True)
