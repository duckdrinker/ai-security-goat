"""
bad_model_source_confirms_deserializer.py
Triggers untrusted-data-reaches-code-sink: an untrusted model source
(from_pretrained, AI-specific source) is downloaded and its checkpoint is
loaded with torch.load(..., weights_only=False) in the same file. The
unsafe-deserializer SAST rule already flags the torch.load call on its own;
the taint chain from an untrusted model source upgrades that finding to
flow-confirmed / high confidence instead of creating a second, duplicate one.
"""
import torch
from huggingface_hub import hf_hub_download

checkpoint_path = hf_hub_download(repo_id="user/custom-checkpoint-model", filename="weights.pt")
state = torch.load(checkpoint_path, weights_only=False)
