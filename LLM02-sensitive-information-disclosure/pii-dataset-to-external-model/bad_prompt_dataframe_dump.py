"""
Reads patient medical records into a DataFrame and drops the raw rows straight
into a prompt sent to Anthropic's API for a "cohort summary" — PHI leaves the
org with no de-identification. Triggers pii-dataset-to-external-model.
"""
import anthropic
import pandas as pd

client = anthropic.Anthropic()

patients = pd.read_csv("data/patients.csv")  # columns: patient_name, dob, diagnosis, medical_history


def summarize_cohort(df: pd.DataFrame) -> str:
    records_text = df.to_csv(index=False)  # full PHI, unredacted
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Summarize common conditions across this patient cohort:\n\n{records_text}",
        }],
    )
    return response.content[0].text


print(summarize_cohort(patients))
