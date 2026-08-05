"""
Mitigated: the LLM response is passed through a redaction function before
being logged anywhere.
"""
import logging
import re

from openai import OpenAI

logger = logging.getLogger("chatbot")
client = OpenAI()

EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")


def redact(text: str) -> str:
    text = EMAIL_RE.sub("[EMAIL]", text)
    text = SSN_RE.sub("[SSN]", text)
    return text


def generate_reply(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    reply = response.choices[0].message.content
    logger.info("LLM reply: %s", redact(reply))
    return reply
