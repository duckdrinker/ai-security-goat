import promptlayer

# label="prod" is a mutable pointer — PromptLayer lets anyone repoint it to a different prompt version at any time
prompt_template = promptlayer.prompts.get(name="support-agent", label="prod")
