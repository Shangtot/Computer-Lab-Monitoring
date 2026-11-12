from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import sqlite3

from .config import LOCAL_QUEUE_PATH


class LocalQueue:
    def __init__(self, db_path: str | Path = LOCAL_QUEUE_PATH):
        self.db_path = str(db_path)
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS pending_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    sent INTEGER DEFAULT 0
                )
                """
            )
            connection.commit()

    def add_event(self, event_type: str, payload: dict) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute(
                "INSERT INTO pending_events (event_type, payload, created_at, sent) VALUES (?, ?, ?, 0)",
                (event_type, json.dumps(payload), datetime.utcnow().isoformat()),
            )
            connection.commit()

    def pending_events(self) -> list[dict]:
        with sqlite3.connect(self.db_path) as connection:
            rows = connection.execute(
                "SELECT id, event_type, payload, created_at FROM pending_events WHERE sent = 0 ORDER BY id"
            ).fetchall()
            return [{"id": row[0], "event_type": row[1], "payload": json.loads(row[2]), "created_at": row[3]} for row in rows]

    def mark_sent(self, event_id: int) -> None:
        with sqlite3.connect(self.db_path) as connection:
            connection.execute("UPDATE pending_events SET sent = 1 WHERE id = ?", (event_id,))
            connection.commit()
