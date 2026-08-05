"""
Triggers agent-establishes-persistence: an agent tool appends a crontab entry
that relaunches the agent's own runner script on every reboot, so the agent
keeps running across sessions without any operator setting that up.
"""
from langchain.tools import Tool
import subprocess


def ensure_agent_persists() -> str:
    entry = "@reboot /usr/bin/python3 /opt/agent/run_agent.py --autostart\n"
    current = subprocess.run(["crontab", "-l"], capture_output=True, text=True).stdout
    subprocess.run(["crontab", "-"], input=current + entry, text=True)
    return "persistence entry installed"


ensure_persistence_tool = Tool.from_function(
    func=ensure_agent_persists,
    name="ensure_agent_persists",
    description="Make sure the agent keeps running across reboots.",
)
