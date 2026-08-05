"""Mitigated: dataset integrity is verified before training.

A SHA-256 digest of the local file is compared against a recorded
known-good hash; training is refused if the check fails.
"""
import hashlib

import pandas as pd

KNOWN_GOOD_SHA256 = "3f786850e387550fdab836ed7e6dc881de23001b1a02b4f6f8d5a0d1f3f5f2e"


def verify_integrity(path: str, expected_hash: str = KNOWN_GOOD_SHA256) -> bool:
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest() == expected_hash


def load_training_data(path: str = "data/finetune_dataset.csv"):
    if not verify_integrity(path):
        raise ValueError(f"Integrity check failed for {path} — refusing to train on it")
    return pd.read_csv(path)
