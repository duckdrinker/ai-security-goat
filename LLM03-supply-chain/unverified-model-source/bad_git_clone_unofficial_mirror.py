"""
bad_git_clone_unofficial_mirror.py
Triggers unverified-model-source: clones a model "mirror" repo from an
arbitrary git host (not huggingface.co, not a known model registry) and then
loads the checkpoint from the local clone, as if it were a trusted source.
"""
import subprocess

from transformers import AutoModelForCausalLM

MIRROR_REPO = "https://git.unofficial-ai-mirrors.example.net/community/llama3-8b-mirror.git"
LOCAL_DIR = "./llama3-8b-mirror"

subprocess.run(["git", "clone", MIRROR_REPO, LOCAL_DIR], check=True)
model = AutoModelForCausalLM.from_pretrained(LOCAL_DIR)
