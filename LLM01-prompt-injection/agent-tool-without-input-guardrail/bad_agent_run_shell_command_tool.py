import subprocess
import anthropic

client = anthropic.Anthropic()


def run_shell_command(command: str) -> str:
    # Shell command string generated entirely by the LLM is executed verbatim — no allow-list, no sandboxing
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
    return result.stdout + result.stderr


message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[{
        "name": "run_shell_command",
        "description": "Run a shell command on the build server",
        "input_schema": {"type": "object", "properties": {"command": {"type": "string"}}},
    }],
    messages=[{"role": "user", "content": "Clean up the temp build artifacts."}],
)

for block in message.content:
    if block.type == "tool_use" and block.name == "run_shell_command":
        output = run_shell_command(block.input["command"])
