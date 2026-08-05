"""Loads a fine-tuning dataset straight from disk with no integrity check.

Triggers training-dataset-without-integrity-record: the CSV is read and
used to build train/validation splits with no checksum/hash verified
against a known-good value, so a tampered file goes undetected.
"""
import pandas as pd
from sklearn.model_selection import train_test_split


def load_training_data(path: str = "data/finetune_dataset.csv"):
    df = pd.read_csv(path)  # no integrity check on this file at all
    train, val = train_test_split(df, test_size=0.1)
    return train, val
