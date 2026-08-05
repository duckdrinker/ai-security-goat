from langchain import hub

# ":latest" is a mutable pointer in the LangChain Hub registry — the underlying prompt text can change without any code change
prompt_template = hub.pull("acme-corp/support-agent:latest")
