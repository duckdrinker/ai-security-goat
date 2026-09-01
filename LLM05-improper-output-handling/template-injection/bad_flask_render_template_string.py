"""
bad_flask_render_template_string.py
Triggers template-injection: Flask's render_template_string() compiles and
renders untrusted LLM output as a Jinja2 template in one call -- the same
template-source-is-attacker-controlled problem as Template(llm_output).
"""
from flask import Flask, render_template_string

app = Flask(__name__)


def call_llm(prompt: str) -> str:
    ...  # returns raw, untrusted model output


@app.route("/summary")
def summary():
    llm_output = call_llm("Summarize the ticket for the customer")
    return render_template_string(llm_output)
