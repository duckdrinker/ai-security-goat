from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(llm, tools)
prompt = SystemMessage("Answer questions about medication dosage and possible drug interactions.")
