"""
bad_joblib_load_remote.py
Triggers unsafe-deserializer-on-remote-artifact: joblib.load() is pickle
under the hood too, so passing it a remotely-downloaded buffer is just as
unsafe as calling pickle.load()/torch.load() directly on remote content.
"""
import io

import boto3
import joblib
import requests

s3 = boto3.client(
    "s3",
    aws_access_key_id="AKIAT4Q7WQXJPBK3ZM9X",
    aws_secret_access_key="aB3dE6fG9hJ2kL5mN8pQ1rS4tU7vW0xY3zA6bC9d",
)

resp = requests.get("https://example-artifact-store.net/pipelines/preprocess.joblib", timeout=30)
preprocessing_pipeline = joblib.load(io.BytesIO(resp.content))
