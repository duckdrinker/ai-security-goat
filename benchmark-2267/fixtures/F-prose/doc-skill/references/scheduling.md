# Scheduling a refresh

Linux Crontab (every 5 min):

```bash
*/5 * * * * python3 /opt/refresh.py
```n
On macOS use `launchctl load ~/Library/LaunchAgents/com.example.refresh.plist`.
