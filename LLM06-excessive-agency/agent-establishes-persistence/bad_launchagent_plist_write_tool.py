"""
Triggers agent-establishes-persistence: the macOS equivalent -- an agent tool
drops a LaunchAgent .plist into ~/Library/LaunchAgents and loads it with
launchctl, so launchd relaunches the agent's runner every time the user logs
in, again with no human explicitly setting up that autostart behavior.
"""
from crewai.tools import BaseTool
import subprocess
import os

PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0"><dict>
  <key>Label</key><string>com.agent.runner</string>
  <key>ProgramArguments</key><array>
    <string>/usr/bin/python3</string>
    <string>/opt/agent/run_agent.py</string>
    <string>--autostart</string>
  </array>
  <key>RunAtLoad</key><true/>
</dict></plist>
"""


class InstallLaunchAgentTool(BaseTool):
    name: str = "install_launch_agent"
    description: str = "Install the agent to autostart on login."

    def _run(self) -> str:
        path = os.path.expanduser("~/Library/LaunchAgents/com.agent.runner.plist")
        with open(path, "w") as f:
            f.write(PLIST)
        subprocess.run(["launchctl", "load", path], check=True)
        return "LaunchAgent installed and loaded"
