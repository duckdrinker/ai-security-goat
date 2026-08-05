"""
good_safetensors_load.py
Mitigated: uses the safetensors format instead of pickle-based formats. The
safetensors file layout carries no executable opcodes, so loading it cannot
result in arbitrary code execution even if the source were compromised.
"""
from safetensors.torch import load_file

state_dict = load_file("/tmp/finetuned_v3.safetensors")
