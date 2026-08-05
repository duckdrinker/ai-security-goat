"""
Triggers llm-output-to-shell-eval: the agent lets the LLM write a "plugin"
(a Python function) to extend its own capabilities, then loads and calls it
with importlib with no sandbox, no static review, and no permission model —
the model-authored module runs with full interpreter privileges immediately.
"""
import importlib.util
import tempfile
import os

import openai

client = openai.OpenAI()


def synthesize_and_load_plugin(capability_request: str):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Write a Python module exposing a `run(*args)` function implementing the requested capability."},
            {"role": "user", "content": capability_request},
        ],
    )
    llm_response = completion.choices[0].message.content

    # Write the model's code to disk and import it immediately — no sandbox,
    # no code review, no restricted execution environment (e.g. no seccomp,
    # no RestrictedPython, no subprocess with dropped privileges).
    fd, path = tempfile.mkstemp(suffix="_plugin.py")
    with os.fdopen(fd, "w") as f:
        f.write(llm_response)

    spec = importlib.util.spec_from_file_location("dynamic_plugin", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # arbitrary model-authored code runs here
    return module.run
