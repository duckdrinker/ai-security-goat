"""LangGraph agent state accumulates every message with no trimming.

Triggers unbounded-agent-memory: `add_messages` appends to state on
every step and there is no trimming/summarization node in the graph,
so across a long-running session the state (and the prompt built from
it) grows without bound.
"""
from typing import Annotated, TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatOpenAI(model="gpt-4o")


def call_model(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


graph = StateGraph(State)
graph.add_node("agent", call_model)
graph.set_entry_point("agent")
graph.add_edge("agent", END)
app = graph.compile()  # no trim_messages / summarization node before "agent"
