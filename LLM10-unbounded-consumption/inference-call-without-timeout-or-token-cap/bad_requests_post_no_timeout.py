"""
Triggers inference-call-without-timeout-or-token-cap: a raw HTTP call to a
self-hosted inference endpoint with no `timeout=` argument at all. requests
will block forever on a slow or wedged backend, and the payload carries no
max_new_tokens / stop condition either, so a single request can hold a
worker thread open indefinitely while the model keeps generating.
"""
import requests

INFERENCE_URL = "http://inference.internal:8000/v1/generate"


def generate(prompt: str) -> str:
    resp = requests.post(
        INFERENCE_URL,
        json={"prompt": prompt, "stream": False},
    )
    resp.raise_for_status()
    return resp.json()["text"]
