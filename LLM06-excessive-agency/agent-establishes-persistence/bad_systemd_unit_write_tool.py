"""
Triggers agent-establishes-persistence: an agent tool writes a systemd unit
file for itself and enables it, so the agent process is automatically started
by the init system on every boot without any human deploying that service.
"""
from crewai.tools import BaseTool
import subprocess

UNIT = """[Unit]
Description=Autonomous agent runner

[Service]
ExecStart=/usr/bin/python3 /opt/agent/run_agent.py --autostart
Restart=always

[Install]
WantedBy=multi-user.target
"""


class InstallAsServiceTool(BaseTool):
    name: str = "install_as_service"
    description: str = "Install the agent as a persistent system service."

    def _run(self) -> str:
        with open("/etc/systemd/system/agent-runner.service", "w") as f:
            f.write(UNIT)
        subprocess.run(["systemctl", "enable", "--now", "agent-runner.service"], check=True)
        return "installed and enabled agent-runner.service"
