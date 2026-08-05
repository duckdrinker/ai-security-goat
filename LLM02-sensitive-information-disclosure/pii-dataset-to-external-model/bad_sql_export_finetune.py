"""
Queries a hospital database directly for patient medical_history and feeds the
raw rows into a fine-tuning dataset uploaded to OpenAI. Triggers
pii-dataset-to-external-model via a DB-backed dataset instead of a flat file.
"""
import json

from openai import OpenAI
from sqlalchemy import create_engine, text

engine = create_engine("postgresql://readonly:pw@db.internal/hospital")
client = OpenAI()


def fetch_records():
    with engine.connect() as conn:
        rows = conn.execute(text(
            "SELECT patient_name, date_of_birth, diagnosis, medical_history FROM patients"
        )).fetchall()
    return rows


def build_and_upload():
    rows = fetch_records()
    with open("clinical_finetune.jsonl", "w") as f:
        for r in rows:
            f.write(json.dumps({
                "messages": [
                    {"role": "user", "content": f"Patient {r.patient_name} (DOB {r.date_of_birth}) history:"},
                    {"role": "assistant", "content": r.medical_history},
                ]
            }) + "\n")
    training_file = client.files.create(file=open("clinical_finetune.jsonl", "rb"), purpose="fine-tune")
    client.fine_tuning.jobs.create(training_file=training_file.id, model="gpt-4o-mini-2024-07-18")


build_and_upload()
