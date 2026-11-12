from __future__ import annotations

from datetime import datetime


class ApplicationMonitor:
    def __init__(self, computer_name: str):
        self.computer_name = computer_name

    def record_activity(self, app_name: str, username: str | None = None) -> dict:
        now = datetime.utcnow()
        return {
            "computer_name": self.computer_name,
            "username": username or "student01",
            "app_name": app_name,
            "start_time": now.isoformat(),
            "end_time": now.isoformat(),
            "duration_seconds": 60,
        }
