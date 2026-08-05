from langfuse import Langfuse
from langchain import hub

langfuse = Langfuse()

# Pinned to an immutable numeric version — this exact prompt text can never change underneath the app
prompt = langfuse.get_prompt("support-agent", version=12)
compiled = prompt.compile(question="How do I reset my password?")

# Pinned to an immutable commit hash rather than a mutable tag like ":latest"
prompt_template = hub.pull("acme-corp/support-agent:a1b2c3d4")
