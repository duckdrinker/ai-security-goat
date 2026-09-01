"""
Mitigated: the template *string* is a static literal owned by the codebase --
only the render() context variable is untrusted. Jinja2's default autoescape
and the fact that the template source itself is not attacker-controlled means
this is the safe pattern, not template injection.
"""
from jinja2 import Template


def call_llm(prompt: str) -> str:
    ...  # returns raw, untrusted model output


user_input = call_llm("What's your name?")

template = Template("Hello, {{ name }}!")
output = template.render(name=user_input)
