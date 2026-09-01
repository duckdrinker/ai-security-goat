"""
Mitigated: the template is loaded from the codebase's own template files via
render_to_string(), not built from untrusted data -- only the context dict
carries untrusted values. A template read from the repo is not attacker-
controlled under a single-file heuristic.
"""
from django.template.loader import render_to_string


def call_llm(prompt: str) -> str:
    ...  # returns raw, untrusted model output


summary_text = call_llm("Summarize the ticket for the customer")
output = render_to_string("tickets/summary.html", {"summary": summary_text})
