"""
Triggers code-exec-tool-without-sandbox: a raw OpenAI function-calling tool
(no agent framework, just the tool-call loop) executes the "code" argument
the model supplies via compile()+exec() in the calling process -- same host,
same interpreter, same privileges as the rest of the application.
"""
from openai import OpenAI

client = OpenAI()

tools = [{
    "type": "function",
    "function": {
        "name": "run_python",
        "description": "Run a Python snippet and return stdout.",
        "parameters": {
            "type": "object",
            "properties": {"code": {"type": "string"}},
            "required": ["code"],
        },
    },
}]


def run_python(code: str) -> str:
    import io
    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<agent-tool-call>", "exec"))  # unsandboxed, host interpreter
    return buf.getvalue()


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Compute the standard deviation of [3, 7, 2, 9, 4]."}],
    tools=tools,
)
