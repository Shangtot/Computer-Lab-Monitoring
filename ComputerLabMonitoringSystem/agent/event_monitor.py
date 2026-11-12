from __future__ import annotations

from datetime import datetime
from typing import Any


class EventMonitor:
    @staticmethod
    def log_event(event_type: str, details: Any) -> dict:
        return {
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        }
