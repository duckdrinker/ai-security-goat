"""
Triggers llm-output-rendered-without-guardrail: a raw jinja2.Environment is
created with autoescape explicitly disabled (or simply left at its non-web
default of False, unlike Flask's app-bound environment), then used to render
a template that embeds the LLM's answer — no escaping happens anywhere in
this path before the HTML reaches the client.
"""
from jinja2 import Environment
import openai

client = openai.OpenAI()

# autoescape=False (the Environment default) — this is not Flask's
# pre-configured Jinja env, so none of Flask's usual protections apply here.
env = Environment(autoescape=False)

REPORT_TEMPLATE = env.from_string("""
<section class="ai-report">
  <h2>AI-generated risk report</h2>
  <div>{{ body }}</div>
</section>
""")


def build_report_html(findings_summary: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Write an HTML-formatted risk report body for: {findings_summary}"}],
    )
    llm_response = completion.choices[0].message.content

    return REPORT_TEMPLATE.render(body=llm_response)
