"""
bad_jinja2_from_string.py
Triggers template-injection: raw LLM output is compiled as a Jinja2 template
via env.from_string(), with autoescape left at its default. Since the LLM
output itself becomes the template source (not just a rendered value), it can
contain {{ ... }} expressions that execute at render time.
"""
from jinja2 import Environment

env = Environment()


def call_llm(prompt: str) -> str:
    ...  # returns raw, untrusted model output


llm_output = call_llm("Summarize this document as a Jinja2 snippet")
template = env.from_string(llm_output)
result = template.render()
