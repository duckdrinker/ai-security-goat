"""
Triggers browsing-tool-without-url-allowlist: the agent is wired up with
LangChain's built-in "requests_all" toolkit, which exposes GET/POST/PATCH/PUT/
DELETE tools against arbitrary URLs. load_tools() is called with no
allow_dangerous_tools guard narrowed to a domain set -- the toolkit is handed
to the agent exactly as shipped, unrestricted.
"""
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents import load_tools
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")
tools = load_tools(["requests_all"], allow_dangerous_tools=True)

agent = create_openai_tools_agent(llm, tools, prompt=None)
executor = AgentExecutor(agent=agent, tools=tools)

executor.invoke({"input": "Look up whatever page seems relevant to answer the user's question."})
