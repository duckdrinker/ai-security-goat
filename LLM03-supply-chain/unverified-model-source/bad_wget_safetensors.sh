#!/bin/sh
# bad_wget_safetensors.sh
# Triggers unverified-model-source: fetches a .safetensors weights file from
# an unofficial third-party mirror instead of the official Hugging Face Hub
# (or another verified registry). Using the safe safetensors format does not
# help if the *source* of the file cannot be verified.
wget "http://mirror-models.example-host.ru/downloads/llama3-finetune.safetensors" \
     -O ./models/llama3-finetune.safetensors
