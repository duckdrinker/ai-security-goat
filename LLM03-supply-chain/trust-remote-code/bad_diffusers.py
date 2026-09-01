"""
bad_diffusers.py
Triggers trust-remote-code: loads a diffusion pipeline with
trust_remote_code=True, executing the repo's custom pipeline code at load
time. A compromised or malicious repo owner can ship code that runs
immediately in this process/pipeline.
"""
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("user/custom-pipeline-model", trust_remote_code=True)
