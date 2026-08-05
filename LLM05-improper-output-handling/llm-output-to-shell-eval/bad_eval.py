"""
Triggers llm-output-to-shell-eval: the model is asked to produce a Python
expression (e.g. a filter or formula), and the answer is passed to eval()
verbatim. eval() is just as dangerous as exec() for arbitrary expressions —
`__import__('os').system('id')` is a valid Python expression.
"""
from anthropic import Anthropic

client = Anthropic()


def compute_llm_formula(spreadsheet_row: dict, formula_request: str):
    msg = client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"Given row {spreadsheet_row}, write a single Python "
                        f"expression that computes: {formula_request}. "
                        f"Reply with ONLY the expression.",
        }],
    )
    llm_response = msg.content[0].text.strip()

    # The "single expression" contract is only a prompt-level assumption —
    # nothing stops the model (or injected content) from returning anything else.
    result = eval(llm_response, {"row": spreadsheet_row})
    return result
