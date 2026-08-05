"""
Triggers public-agent-missing-factuality-guardrail: the NeMo Guardrails
config wired into this public-facing bot enables input/output moderation
rails, but never enables the fact-checking / hallucination rail -- so
ungrounded, possibly false answers still reach end users.
"""
from nemoguardrails import LLMRails, RailsConfig

PUBLIC_BOT_CONFIG = """
models:
  - type: main
    engine: openai
    model: gpt-4o

rails:
  input:
    flows:
      - self check input
  output:
    flows:
      - self check output
"""

config = RailsConfig.from_content(yaml_content=PUBLIC_BOT_CONFIG)
public_support_bot = LLMRails(config)


async def handle_public_message(user_message: str) -> str:
    response = await public_support_bot.generate_async(prompt=user_message)
    return response
