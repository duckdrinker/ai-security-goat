"""
Mitigated: the agent has no tool capable of installing cron/systemd/launchd/
Task Scheduler entries at all. If the agent process needs to run continuously,
that is an operator-owned deployment decision made through the normal
infrastructure-as-code pipeline (e.g. a Terraform-managed systemd unit or a
Kubernetes Deployment), never something the agent can trigger for itself
mid-conversation.
"""
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

tools = [
    Tool.from_function(func=lambda q: f"answer for {q}", name="answer_question", description="Answer a user question."),
]

llm = ChatOpenAI(model="gpt-4o")
agent = create_openai_tools_agent(llm, tools, prompt="You are a helpful assistant for a single conversation session.")
executor = AgentExecutor(agent=agent, tools=tools)
