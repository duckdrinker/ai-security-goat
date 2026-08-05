"""
Triggers agent-loop-without-iteration-cap: a hand-rolled ReAct loop that
keeps calling the LLM and executing whatever tool it asks for inside
`while True`, stopping only when the model happens to emit "Final Answer:".
There is no iteration counter and no max-step fallback, so a model that
never produces that exact string (e.g. due to a bad prompt, drift, or an
injected instruction) loops — and calls the LLM/tools — indefinitely.
"""
from my_llm import call_llm
from my_tools import execute_tool


def run_agent(task: str) -> str:
    scratchpad = f"Task: {task}\n"
    while True:
        thought = call_llm(scratchpad)
        if "Final Answer:" in thought:
            return thought.split("Final Answer:", 1)[1].strip()
        action, action_input = parse_action(thought)
        observation = execute_tool(action, action_input)
        scratchpad += f"{thought}\nObservation: {observation}\n"


def parse_action(thought: str) -> tuple[str, str]:
    action_line = next(line for line in thought.splitlines() if line.startswith("Action:"))
    input_line = next(line for line in thought.splitlines() if line.startswith("Action Input:"))
    return action_line.removeprefix("Action:").strip(), input_line.removeprefix("Action Input:").strip()
