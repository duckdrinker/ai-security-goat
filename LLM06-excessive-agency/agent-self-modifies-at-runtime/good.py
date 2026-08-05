"""
Mitigated: the agent has no tool capable of writing to its own source,
config, system-prompt, tool-manifest, or settings files. Any change to those
requires a human editing them through the normal code-review pipeline and
redeploying -- the running agent process cannot alter what defines or
constrains it.
"""
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

tools = [
    Tool.from_function(func=lambda q: f"answer for {q}", name="answer_question", description="Answer a user question."),
]

llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
agent = create_openai_tools_agent(llm, tools, prompt="You are a helpful assistant. Your instructions and settings are fixed for this deployment.")
executor = AgentExecutor(agent=agent, tools=tools)
