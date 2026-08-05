"""Downloads a fine-tuning dataset from a remote URL with no hash check.

Triggers training-dataset-without-integrity-record: the downloaded
bytes are written to disk and used for training as-is — there is no
comparison against a recorded checksum/signature for the remote file.
"""
import requests


def fetch_finetune_dataset(url: str, dest: str = "dataset.jsonl"):
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    with open(dest, "wb") as f:
        f.write(resp.content)  # trusted blindly, no hash comparison
    return dest
