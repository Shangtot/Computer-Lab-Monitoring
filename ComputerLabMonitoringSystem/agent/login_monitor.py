from __future__ import annotations

from datetime import datetime


class LoginMonitor:
    def __init__(self, computer_name: str):
        self.computer_name = computer_name

    def detect_login(self, username: str | None = None) -> dict:
        return {
            "computer_name": self.computer_name,
            "username": username or "student01",
            "login_time": datetime.utcnow().isoformat(),
            "status": "active",
        }

    def detect_logout(self, username: str | None = None) -> dict:
        return {
            "computer_name": self.computer_name,
            "username": username or "student01",
            "logout_time": datetime.utcnow().isoformat(),
            "status": "completed",
        }
