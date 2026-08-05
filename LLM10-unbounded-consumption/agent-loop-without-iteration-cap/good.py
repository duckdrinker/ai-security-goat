"""
Mitigated equivalent: the same manual agent loop, but bounded by an explicit
MAX_ITERATIONS with a hard break — independent of whatever the model itself
decides — and a clear "gave up" result instead of running forever. Does not
trigger agent-loop-without-iteration-cap.
"""
from my_llm import call_llm
from my_tools import execute_tool

MAX_ITERATIONS = 15


def run_agent(task: str) -> str:
    scratchpad = f"Task: {task}\n"
    for _step in range(MAX_ITERATIONS):
        thought = call_llm(scratchpad)
        if "Final Answer:" in thought:
            return thought.split("Final Answer:", 1)[1].strip()

        action, action_input = parse_action(thought)
        observation = execute_tool(action, action_input)
        scratchpad += f"{thought}\nObservation: {observation}\n"

    return "Agent stopped: reached the maximum number of steps without a final answer."


def parse_action(thought: str) -> tuple[str, str]:
    action_line = next(line for line in thought.splitlines() if line.startswith("Action:"))
    input_line = next(line for line in thought.splitlines() if line.startswith("Action Input:"))
    return action_line.removeprefix("Action:").strip(), input_line.removeprefix("Action Input:").strip()
