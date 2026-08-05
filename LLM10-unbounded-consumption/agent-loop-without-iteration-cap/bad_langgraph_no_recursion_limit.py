"""
Triggers agent-loop-without-iteration-cap: a LangGraph ReAct-style graph is
compiled and invoked with no `recursion_limit` in the run config. The
"agent" node keeps cycling back into "tools" for as long as the model
emits a tool call, and nothing in the graph or the invocation bounds how
many times that cycle can happen — a model that never emits a final answer
(e.g. stuck oscillating between two tool calls) runs forever.
"""
from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from my_llm import call_model  # returns an AIMessage, may include tool_calls
from my_tools import TOOLS

graph = StateGraph(dict)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(TOOLS))
graph.add_edge("tools", "agent")
graph.add_conditional_edges(
    "agent",
    lambda state: "tools" if state["messages"][-1].tool_calls else END,
)
graph.set_entry_point("agent")

app = graph.compile()


def run_agent(user_task: str) -> str:
    result = app.invoke({"messages": [{"role": "user", "content": user_task}]})
    return result["messages"][-1].content
