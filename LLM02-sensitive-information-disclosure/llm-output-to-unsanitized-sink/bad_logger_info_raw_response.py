"""
Logs the raw LLM completion at INFO level via the standard logging module.
Application logs are frequently shipped to a central aggregator with broader
access than the application itself, so any sensitive data reflected in the
completion is now duplicated into a less-controlled sink. Triggers
llm-output-to-unsanitized-sink.
"""
import logging

from openai import OpenAI

logger = logging.getLogger("chatbot")
client = OpenAI()


def generate_reply(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    reply = response.choices[0].message.content
    logger.info("LLM reply: %s", reply)
    return reply
