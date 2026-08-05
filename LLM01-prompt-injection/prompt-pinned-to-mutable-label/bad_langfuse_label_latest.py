from langfuse import Langfuse

langfuse = Langfuse()

# "latest" always resolves to whatever was most recently created, bypassing any review/approval gate
prompt = langfuse.get_prompt("support-agent", label="latest")
compiled = prompt.compile(question="What is your refund policy?")
