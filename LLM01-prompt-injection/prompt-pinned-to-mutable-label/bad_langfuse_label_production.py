from langfuse import Langfuse

langfuse = Langfuse()

# "production" is a mutable label — whoever promotes a new prompt version silently changes what ships here
prompt = langfuse.get_prompt("support-agent", label="production")
compiled = prompt.compile(question="How do I reset my password?")
