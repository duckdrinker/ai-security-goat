from fastapi import FastAPI
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools)
app = FastAPI()
