"""
bad_torch_load_download_cache.py
Triggers unsafe-deserializer-on-remote-artifact: downloads a checkpoint to a
local cache file first, then calls torch.load() on it with default settings
(weights_only=False on older torch versions). Saving to disk in between does
not make the deserialization step any safer.
"""
import urllib.request

import torch

CHECKPOINT_URL = "https://cdn.example-model-host.io/checkpoints/finetuned_v3.pt"
LOCAL_PATH = "/tmp/finetuned_v3.pt"

urllib.request.urlretrieve(CHECKPOINT_URL, LOCAL_PATH)
state_dict = torch.load(LOCAL_PATH)
