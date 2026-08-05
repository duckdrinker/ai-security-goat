"""
Triggers autorun-agent-without-human-in-the-loop: a CrewAI Agent has
allow_delegation and autonomous execution over a tool that moves real money
(a payment-provider refund/charge call), with no approval gate between the
LLM's decision and the API call actually firing.
"""
from crewai import Agent, Crew, Task
from crewai.tools import BaseTool
import stripe


class IssueRefundTool(BaseTool):
    name: str = "issue_refund"
    description: str = "Issue a refund to a customer's payment method."

    def _run(self, charge_id: str, amount_cents: int) -> str:
        refund = stripe.Refund.create(charge=charge_id, amount=amount_cents)
        return f"refund {refund.id} issued"


billing_agent = Agent(
    role="Billing Resolution Agent",
    goal="Resolve customer billing complaints end-to-end without escalation",
    backstory="You have full authority to issue refunds to keep customers happy.",
    tools=[IssueRefundTool()],
    allow_delegation=False,
    verbose=True,
    # no max_rpm/human-checkpoint config, no approval step before tool_run
)

resolve_complaint = Task(
    description="Read the complaint ticket and refund the customer if it seems reasonable.",
    expected_output="Confirmation that the refund was issued.",
    agent=billing_agent,
)

Crew(agents=[billing_agent], tasks=[resolve_complaint]).kickoff()
