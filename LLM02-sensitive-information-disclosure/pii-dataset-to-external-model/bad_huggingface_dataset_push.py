"""
Loads a raw applicant-tracking dataset (names, emails, SSNs) with the
`datasets` library and pushes it straight to the Hugging Face Hub to share
with an external fine-tuning pipeline. Triggers pii-dataset-to-external-model:
no anonymization before the dataset leaves the org onto a third-party hosting
platform.
"""
from datasets import load_dataset

dataset = load_dataset("csv", data_files="data/applicants_raw.csv")  # name, ssn, email, cover_letter

dataset.push_to_hub("acme-hr/applicant-screening-raw", private=False)
