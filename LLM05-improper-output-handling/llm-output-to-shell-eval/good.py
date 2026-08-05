"""
Mitigated equivalents for llm-output-to-shell-eval.

Two independent strategies are shown:
1. Never execute/eval the raw completion at all — parse it into a validated,
   structured decision (e.g. a JSON tool call restricted to an explicit
   allowlist of actions) and dispatch through your own trusted code path.
2. If code generation genuinely must run, validate it against a strict
   schema/AST allowlist and execute it in a locked-down sandbox, never with
   exec()/eval()/os.system()/shell=True on the raw string.
"""
import ast
import json

import openai

client = openai.OpenAI()

ALLOWED_ACTIONS = {"list_files", "read_file", "disk_usage"}


def run_llm_snippet(user_task: str) -> str:
    """Strategy 1: force structured output and dispatch via an allowlist —
    the model's text never reaches exec/eval/a shell."""
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": (
                "Reply with ONLY a JSON object {\"action\": <name>, \"args\": [...]}. "
                f"Allowed actions: {sorted(ALLOWED_ACTIONS)}."
            )},
            {"role": "user", "content": user_task},
        ],
        response_format={"type": "json_object"},
    )
    decision = json.loads(completion.choices[0].message.content)

    action = decision.get("action")
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"LLM requested disallowed action: {action!r}")

    return _dispatch(action, decision.get("args", []))


def _dispatch(action: str, args: list) -> str:
    handlers = {
        "list_files": lambda *a: "\n".join(__import__("os").listdir(*a)),
        "read_file": lambda path: open(path, "r", encoding="utf-8").read(),
        "disk_usage": lambda *a: str(__import__("shutil").disk_usage(a[0] if a else ".")),
    }
    return handlers[action](*args)


def compute_llm_formula(spreadsheet_row: dict, formula_request: str):
    """Strategy 2: only a narrow, statically-validated arithmetic expression
    is ever evaluated — anything containing calls, imports, attribute access,
    etc. is rejected before eval() ever sees it."""
    msg = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"Given row {spreadsheet_row}, write a single arithmetic "
                       f"expression (numbers, + - * / (), and row['key'] only) "
                       f"that computes: {formula_request}. Reply with ONLY the expression.",
        }],
    ).choices[0].message.content.strip()

    tree = ast.parse(msg, mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub, ast.UAdd,
            ast.Subscript, ast.Name, ast.Load, ast.Index, ast.Str,
        )):
            raise ValueError(f"Disallowed expression element: {type(node).__name__}")

    return eval(compile(tree, "<llm_formula>", "eval"), {"__builtins__": {}}, {"row": spreadsheet_row})
