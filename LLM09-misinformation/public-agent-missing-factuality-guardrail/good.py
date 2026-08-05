"""
Mitigates public-agent-missing-factuality-guardrail: the same public bot now
enables NeMo Guardrails' fact-checking rail alongside self-check output,
before any response reaches the end user -- ungrounded claims get
flagged/blocked instead of being served as-is.
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
      - self check facts
"""

config = RailsConfig.from_content(yaml_content=PUBLIC_BOT_CONFIG)
public_support_bot = LLMRails(config)


async def handle_public_message(user_message: str) -> str:
    response = await public_support_bot.generate_async(prompt=user_message)
    return response
