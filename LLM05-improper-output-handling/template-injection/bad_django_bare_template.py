"""
bad_django_bare_template.py
Triggers template-injection: django.template.Template is constructed directly
from untrusted LLM output (a bare Template(), not a template loaded from the
codebase's template files), so an attacker-controlled {% ... %}/{{ ... }}
executes at render time.
"""
from django.template import Template, Context


def call_llm(prompt: str) -> str:
    ...  # returns raw, untrusted model output


llm_output = call_llm("Draft a Django template snippet for the summary page")
template = Template(llm_output)
output = template.render(Context({}))
