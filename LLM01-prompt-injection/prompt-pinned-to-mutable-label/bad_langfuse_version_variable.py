import os
from langfuse import Langfuse

langfuse = Langfuse()
cfg_version = os.environ.get("SUPPORT_PROMPT_VERSION")

# version is bound to a variable, not a constant — not a provable immutable pin
prompt = langfuse.get_prompt("support-agent", version=cfg_version)
compiled = prompt.compile(question="How do I cancel my subscription?")
