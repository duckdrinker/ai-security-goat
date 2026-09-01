"""
bad_jinja2_fstring.py
Triggers template-injection: untrusted agent output is interpolated directly
into the Jinja2 template *string* itself (not just the render context), so an
attacker who controls that output controls the template source -- e.g.
{{ __import__('os').system('id') }} achieves RCE.
"""
from jinja2 import Template


def call_llm(prompt: str) -> str:
    ...  # returns raw, untrusted model output


search_results = call_llm("latest security advisories")

template = Template(f"Search results: {search_results}")
output = template.render()
