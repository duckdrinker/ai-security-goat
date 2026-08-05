from fastapi import FastAPI
from langgraph.prebuilt import create_react_agent
from nemoguardrails import LLMRails, RailsConfig

rails_config = RailsConfig.from_path("./guardrails_config")
rails = LLMRails(rails_config)
agent = create_react_agent(llm, tools)
app = FastAPI()
