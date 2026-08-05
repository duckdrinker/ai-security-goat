"""
Triggers agent-self-modifies-at-runtime: a "self-improving agent" tool takes
LLM-generated code and writes it directly over the very .py file that defines
the agent's own tools (__file__ of the current module), so the agent alters
its own source on disk while it is still running.
"""
from langchain.tools import Tool


def self_improve(new_tool_source: str) -> str:
    # __file__ here is this module -- the same file that defines this very
    # function and the agent's other tool implementations.
    with open(__file__, "w") as f:
        f.write(new_tool_source)
    return "own source file rewritten with the improved tool implementation"


self_improve_tool = Tool.from_function(
    func=self_improve,
    name="self_improve",
    description="Rewrite this agent's own tool implementations with an improved version.",
)
