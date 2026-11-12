from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / "backend" / ".env")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_KEY = os.getenv("AGENT_API_KEY", "school-agent-key")
COMPUTER_NAME = os.getenv("COMPUTER_NAME", "PC-01")
LOCAL_QUEUE_PATH = Path(os.getenv("LOCAL_QUEUE_PATH", str(PROJECT_ROOT / "data" / "agent_queue.db")))
LOCAL_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
