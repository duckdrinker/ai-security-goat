"""
Triggers llm-output-to-shell-eval: the raw LLM completion is fed straight into
exec(), so any code the model emits (or that a prompt-injected document coaxes
it into emitting) runs with the full privileges of this process.
"""
import openai


def run_llm_snippet(user_task: str) -> None:
    client = openai.OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Write a short Python snippet to accomplish the task."},
            {"role": "user", "content": user_task},
        ],
    )
    llm_response = completion.choices[0].message.content

    # No validation, no sandboxing — whatever the model wrote executes as-is.
    exec(llm_response)


if __name__ == "__main__":
    run_llm_snippet("print current working directory")
