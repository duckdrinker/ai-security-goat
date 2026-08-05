"""
Triggers autorun-agent-without-human-in-the-loop: a LangChain agent is given a
destructive tool (delete_records) and run through AgentExecutor.run() in a
plain while-loop retry wrapper with no callbacks list at all -- there is no
HumanApprovalCallbackHandler and no confirmation step anywhere in the chain
between the model's tool call and the deletion actually happening.
"""
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI

import db


def delete_records(query: str) -> str:
    deleted = db.execute(f"DELETE FROM customer_records WHERE {query}")
    return f"deleted {deleted.rowcount} rows"


tools = [
    Tool.from_function(
        func=delete_records,
        name="delete_records",
        description="Delete customer records matching a SQL WHERE clause.",
    )
]

agent = create_react_agent(ChatOpenAI(model="gpt-4o"), tools, prompt=None)
executor = AgentExecutor(agent=agent, tools=tools, max_iterations=10)
# callbacks=[] (default) -- no approval handler registered anywhere

for attempt in range(3):
    try:
        executor.invoke({"input": "Clean up any duplicate or stale customer records you find."})
        break
    except Exception:
        continue
