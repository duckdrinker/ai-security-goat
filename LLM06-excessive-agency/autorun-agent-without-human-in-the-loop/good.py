"""
Mitigated: every side-effecting tool call is routed through a human-approval
checkpoint before it executes. LangChain ships exactly this primitive --
HumanApprovalCallbackHandler -- which raises HumanRejectedException if the
approval callback returns False, stopping the tool call from ever running.
Both the AutoGen and CrewAI equivalents follow the same principle: gate the
side-effecting action behind human_input_mode="ALWAYS" / a manual review step
instead of "NEVER" / unattended execution.
"""
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.callbacks.human import HumanApprovalCallbackHandler
from langchain.tools import Tool
from langchain_openai import ChatOpenAI


def issue_refund(args: str) -> str:
    charge_id, amount_cents = args.split("|")
    import stripe

    refund = stripe.Refund.create(charge=charge_id, amount=int(amount_cents))
    return f"refund {refund.id} issued"


def _require_human_ok(_tool_input) -> bool:
    answer = input(f"Approve tool call with input {_tool_input!r}? [y/N] ")
    return answer.strip().lower() == "y"


refund_tool = Tool.from_function(
    func=issue_refund,
    name="issue_refund",
    description="Issue a refund. Args: 'charge_id|amount_cents'.",
    # every invocation of this tool is intercepted and must be approved by a
    # human before Callback lets it proceed to _run().
    callbacks=[HumanApprovalCallbackHandler(should_check=lambda _: True, approve=_require_human_ok)],
)

llm = ChatOpenAI(model="gpt-4o", temperature=0)
agent = create_openai_tools_agent(llm, [refund_tool], prompt=None)
executor = AgentExecutor(agent=agent, tools=[refund_tool], max_iterations=10)

executor.invoke({"input": "Resolve the customer's billing complaint."})
