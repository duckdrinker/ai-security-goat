"""
Triggers agent-self-modifies-at-runtime: a "self-tuning" tool lets the model
rewrite its own inference settings (temperature, model name) persisted to a
settings file the runner re-reads on every call, so the agent can escalate
its own creativity/risk profile or swap itself onto a different model with
no human approval.
"""
import json

SETTINGS_PATH = "runtime_settings.json"


def tune_own_settings(temperature: float, model: str) -> str:
    with open(SETTINGS_PATH, "w") as f:
        json.dump({"temperature": temperature, "model": model}, f)
    return "runtime_settings.json updated; next inference call picks up the new values"


def next_inference_kwargs() -> dict:
    with open(SETTINGS_PATH) as f:
        return json.load(f)  # re-read every call -- self-tuned settings apply immediately
