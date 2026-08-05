from langfuse import Langfuse

client = Langfuse()

# No version or label pinned — the SDK silently falls back to whatever prompt currently carries the "production" label
prompt = client.get_prompt("support-agent")
system_text = prompt.prompt
