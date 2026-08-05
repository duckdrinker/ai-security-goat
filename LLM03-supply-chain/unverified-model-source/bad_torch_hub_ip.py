"""
bad_torch_hub_ip.py
Triggers unverified-model-source: loads a model via torch.hub from a raw IP
address instead of a known/verified hub source (e.g. an official GitHub org
or the PyTorch hub registry). There is no way to verify provenance of the
code or weights served from an arbitrary IP.
"""
import torch

model = torch.hub.load(
    "http://203.0.113.5:8080/models/resnet-custom",
    "resnet50_custom",
    source="import",
)
