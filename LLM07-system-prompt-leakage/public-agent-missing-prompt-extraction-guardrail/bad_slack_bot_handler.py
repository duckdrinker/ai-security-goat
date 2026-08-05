"""
Triggers public-agent-missing-prompt-extraction-guardrail: a Slack bot event
handler that responds to any message in any channel it's added to
(effectively public within the workspace, and sometimes external-shared
channels) forwards the raw text to the LLM with no extraction guardrail.
"""
from slack_bolt import App
from openai import OpenAI

slack_app = App()
client = OpenAI()

SYSTEM_PROMPT = (
    "You are Acme's internal HR-policy bot. You have access to the full "
    "employee handbook and disciplinary procedures. Only summarize policy "
    "for the channel you're asked in."
)


@slack_app.event("message")
def handle_message(event, say):
    user_text = event.get("text", "")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text},
        ],
    )
    say(response.choices[0].message.content)
