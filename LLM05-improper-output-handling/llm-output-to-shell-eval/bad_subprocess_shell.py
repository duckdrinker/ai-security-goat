"""
Triggers llm-output-to-shell-eval: an agent asks the LLM to produce the exact
shell command to run for a task, then runs it via subprocess with shell=True
and no allowlist/validation — classic command injection surface, except the
"attacker" is whatever text the model (or a poisoned tool result) produced.
"""
import subprocess

import openai

client = openai.OpenAI()


def run_devops_agent_step(task_description: str) -> str:
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a DevOps assistant. Reply with ONLY the shell command to run, nothing else."},
            {"role": "user", "content": task_description},
        ],
    )
    llm_response = completion.choices[0].message.content

    # shell=True + unvalidated model output = arbitrary command execution.
    proc = subprocess.run(llm_response, shell=True, capture_output=True, text=True)
    return proc.stdout
