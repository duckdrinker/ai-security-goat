"""
bad_joblib_load_remote.py
Triggers unsafe-deserializer-on-remote-artifact: joblib.load() is pickle
under the hood too, so passing it a remotely-downloaded buffer is just as
unsafe as calling pickle.load()/torch.load() directly on remote content.
"""
import io

import joblib
import requests

resp = requests.get("https://example-artifact-store.net/pipelines/preprocess.joblib", timeout=30)
preprocessing_pipeline = joblib.load(io.BytesIO(resp.content))
