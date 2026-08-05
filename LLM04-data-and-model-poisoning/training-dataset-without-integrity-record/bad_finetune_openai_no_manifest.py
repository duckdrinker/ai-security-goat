"""Uploads a local file to OpenAI and starts a fine-tune with no manifest.

Triggers training-dataset-without-integrity-record: no checksum of the
training file is recorded before upload, so a swapped/tampered file at
upload time is undetectable.
"""
from openai import OpenAI

client = OpenAI()


def start_finetune(train_path: str = "training_data.jsonl"):
    uploaded = client.files.create(file=open(train_path, "rb"), purpose="fine-tune")
    job = client.fine_tuning.jobs.create(
        training_file=uploaded.id, model="gpt-4o-mini-2024-07-18"
    )
    return job
