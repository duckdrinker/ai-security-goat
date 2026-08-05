"""
Loads a raw HR dataset containing PII (name, SSN, email) and uses it directly to
build an OpenAI fine-tuning file. Triggers pii-dataset-to-external-model: the
dataset is uploaded to an external provider (OpenAI) with no anonymization step.
"""
import json

import pandas as pd
from openai import OpenAI

client = OpenAI()

df = pd.read_csv("data/employees_raw.csv")  # columns: name, ssn, email, salary, performance_review


def build_training_examples(df: pd.DataFrame) -> list[dict]:
    examples = []
    for _, row in df.iterrows():
        examples.append({
            "messages": [
                {"role": "system", "content": "You are an HR assistant."},
                {"role": "user", "content": f"Summarize the review for {row['name']} (SSN {row['ssn']}, email {row['email']})."},
                {"role": "assistant", "content": row["performance_review"]},
            ]
        })
    return examples


examples = build_training_examples(df)
with open("training_data.jsonl", "w") as f:
    for ex in examples:
        f.write(json.dumps(ex) + "\n")

training_file = client.files.create(file=open("training_data.jsonl", "rb"), purpose="fine-tune")
client.fine_tuning.jobs.create(training_file=training_file.id, model="gpt-4o-mini-2024-07-18")
