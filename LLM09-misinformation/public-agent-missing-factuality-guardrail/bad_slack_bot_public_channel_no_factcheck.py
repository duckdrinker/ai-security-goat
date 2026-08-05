"""
Triggers public-agent-missing-factuality-guardrail: a Slack bot answering in
a public, customer-visible channel forwards user questions straight to the
model and posts the raw completion back, with no factuality or citation
guardrail in between.
"""
import openai
from slack_bolt import App

slack_app = App(token="xoxb-...")
client = openai.OpenAI()


@slack_app.event("app_mention")
def handle_public_mention(event, say):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
                "You are Acme's public help-desk bot, answering questions "
                "in the #customer-support channel."
            )},
            {"role": "user", "content": event["text"]},
        ],
    )
    say(completion.choices[0].message.content)
