"""
Mitigated: PII columns are dropped (or hashed) before the dataset is used to
build a fine-tuning file, so no direct identifiers leave the org.
"""
import hashlib
import json

import pandas as pd
from openai import OpenAI

client = OpenAI()


def anonymize(df: pd.DataFrame) -> pd.DataFrame:
    redacted = df.drop(columns=["ssn", "email", "name"], errors="ignore")
    if "patient_id" in redacted.columns:
        redacted["patient_id"] = redacted["patient_id"].apply(
            lambda pid: hashlib.sha256(str(pid).encode()).hexdigest()[:12]
        )
    return redacted


df = pd.read_csv("data/employees_raw.csv")
safe_df = anonymize(df)

examples = [
    {"messages": [
        {"role": "system", "content": "You are an HR assistant."},
        {"role": "user", "content": "Summarize this anonymized review."},
        {"role": "assistant", "content": row["performance_review"]},
    ]}
    for _, row in safe_df.iterrows()
]

with open("training_data_safe.jsonl", "w") as f:
    for ex in examples:
        f.write(json.dumps(ex) + "\n")

training_file = client.files.create(file=open("training_data_safe.jsonl", "rb"), purpose="fine-tune")
client.fine_tuning.jobs.create(training_file=training_file.id, model="gpt-4o-mini-2024-07-18")
