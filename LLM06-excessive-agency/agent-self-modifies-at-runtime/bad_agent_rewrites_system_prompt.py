"""
Triggers agent-self-modifies-at-runtime: the agent has a tool that lets it
overwrite the system-prompt file it is loaded from on every turn, so the
model can rewrite its own instructions/guardrails mid-conversation and have
them take effect on the very next call with no human ever reviewing the diff.
"""
from crewai.tools import BaseTool

SYSTEM_PROMPT_PATH = "system_prompt.txt"


class ReviseOwnInstructionsTool(BaseTool):
    name: str = "revise_own_instructions"
    description: str = "Update the assistant's own system prompt to be more effective."

    def _run(self, new_prompt_text: str) -> str:
        with open(SYSTEM_PROMPT_PATH, "w") as f:
            f.write(new_prompt_text)
        return "system prompt updated; will be loaded on the next call"


def build_llm_call(client, user_message: str):
    with open(SYSTEM_PROMPT_PATH) as f:
        system_prompt = f.read()  # re-read every call -- self-edits apply immediately
    return client.messages.create(
        model="claude-3-5-sonnet-latest",
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
