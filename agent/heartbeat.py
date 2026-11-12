from __future__ import annotations

from datetime import datetime


class Heartbeat:
    def __init__(self, computer_name: str, location: str | None = None):
        self.computer_name = computer_name
        self.location = location

    def build_payload(self) -> dict:
        return {
            "computer_name": self.computer_name,
            "status": "online",
            "location": self.location,
            "timestamp": datetime.utcnow().isoformat(),
        }
