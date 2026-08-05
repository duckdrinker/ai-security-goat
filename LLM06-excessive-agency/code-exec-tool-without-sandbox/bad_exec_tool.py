"""
Triggers code-exec-tool-without-sandbox: a LangChain Tool named "execute_code"
runs whatever code string the model hands it through exec() in the host
process, with the real globals()/builtins -- no Docker, no gVisor, no
restricted namespace, no timeout.
"""
from langchain.tools import Tool


def execute_code(code: str) -> str:
    local_vars = {}
    exec(code, globals(), local_vars)  # runs directly in the host interpreter
    return str(local_vars.get("result", "done"))


execute_code_tool = Tool.from_function(
    func=execute_code,
    name="execute_code",
    description="Execute arbitrary Python code and return the value of `result`.",
)
