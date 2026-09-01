"""
bad_mako.py
Triggers template-injection: the Mako template *content* itself is built from
untrusted LLM output, so an attacker-controlled ${...} expression executes at
render time.
"""
from mako.template import Template


def call_llm(prompt: str) -> str:
    ...  # returns raw, untrusted model output


llm_output = call_llm("Draft a Mako report snippet")
template = Template(f"Report: {llm_output}")
result = template.render()
