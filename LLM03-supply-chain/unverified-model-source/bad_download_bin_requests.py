"""
bad_download_bin_requests.py
Triggers unverified-model-source: downloads a raw .bin weights file from a
generic, unofficial file-hosting URL (not a known model registry) before
loading it into memory.
"""
import requests

WEIGHTS_URL = "https://free-file-host.example.org/uploads/best_model_final_v2.bin"

response = requests.get(WEIGHTS_URL, timeout=30)
with open("best_model_final_v2.bin", "wb") as f:
    f.write(response.content)
