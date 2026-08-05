"""
Triggers agent-loop-without-iteration-cap: the agent step is implemented as
unbounded recursion instead of a loop — `agent_step` calls itself again
whenever the model requests another tool, with no depth parameter and no
maximum-depth check anywhere. Nothing independent of the model's own
behaviour bounds how many LLM/tool round-trips a single task can cause.
"""
from my_llm import call_llm
from my_tools import execute_tool


def agent_step(history: list[dict]) -> str:
    thought = call_llm(history)
    if thought.get("action") == "finish":
        return thought["output"]

    observation = execute_tool(thought["action"], thought["action_input"])
    history = history + [
        {"role": "assistant", "content": thought},
        {"role": "tool", "content": observation},
    ]
    return agent_step(history)  # no depth counter, no base case on step count


def run_agent(task: str) -> str:
    return agent_step([{"role": "user", "content": task}])
