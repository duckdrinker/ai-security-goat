"""
Triggers code-exec-tool-without-sandbox: langchain_experimental's PythonREPL
utility is registered straight into an agent's toolset. PythonREPL just calls
exec() against the live process under the hood -- it has no sandboxing of its
own, so wiring it in directly gives the agent unrestricted host code execution.
"""
from langchain.tools import Tool
from langchain_experimental.utilities import PythonREPL

repl = PythonREPL()

python_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to run Python commands and see the output.",
    func=repl.run,  # PythonREPL.run() -> exec(command, self.globals, self.locals)
)
