"""
Triggers public-agent-missing-factuality-guardrail: the agent is declared for
the public-facing website widget (exposed to anonymous visitors), but its
config only lists a profanity filter -- no factuality/citation guardrail is
attached to the pipeline for this public-facing agent.
"""
from dataclasses import dataclass, field


@dataclass
class AgentConfig:
    name: str
    channel: str
    public: bool
    guardrails: list = field(default_factory=list)


website_widget_agent = AgentConfig(
    name="acme-website-assistant",
    channel="web-widget",
    public=True,
    guardrails=["profanity-filter"],
)


def build_agent(config: AgentConfig):
    # ... wires config.guardrails into the LLM call pipeline. No factuality
    # or citation-check guardrail is present for this public-facing agent.
    return config
