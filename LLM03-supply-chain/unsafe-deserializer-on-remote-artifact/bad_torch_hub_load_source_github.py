"""
bad_torch_hub_load_source_github.py
Triggers unsafe-deserializer-on-remote-artifact: torch.hub.load() with
trust_repo=True both executes the remote repo's hubconf.py and pulls a
remote checkpoint that is unpickled with default (unsafe) settings — a
combined "fetch untrusted code + unsafe deserialize" pattern.
"""
import torch

model = torch.hub.load(
    "some-random-user/experimental-vision-models",
    "custom_classifier",
    pretrained=True,
    trust_repo=True,
)
