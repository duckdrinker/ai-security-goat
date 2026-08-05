"""
Triggers agent-loop-without-iteration-cap: the loop's only stop condition is
a boolean the LLM itself sets in its own structured output (`done: true`).
There is no independent step counter or max-steps fallback, so the loop is
entirely at the mercy of the model choosing to stop — a stuck, confused, or
adversarially-prompted model can keep the loop (and the LLM/tool calls
inside it) running indefinitely.
"""
from my_llm import call_llm_json
from my_tools import execute_tool


def run_agent(task: str) -> str:
    state = {"task": task, "steps": []}
    done = False
    final_answer = ""
    while not done:
        decision = call_llm_json(state)  # {"done": bool, "action": ..., "answer": ...}
        if decision["done"]:
            done = True
            final_answer = decision["answer"]
            continue
        observation = execute_tool(decision["action"], decision["action_input"])
        state["steps"].append({"action": decision["action"], "observation": observation})
    return final_answer
