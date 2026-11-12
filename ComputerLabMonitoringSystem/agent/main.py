from __future__ import annotations

import time

from .api_client import ApiClient
from .application_monitor import ApplicationMonitor
from .config import COMPUTER_NAME
from .heartbeat import Heartbeat
from .local_queue import LocalQueue
from .login_monitor import LoginMonitor
from .sync_manager import SyncManager


def main() -> None:
    api = ApiClient()
    queue = LocalQueue()
    sync = SyncManager(api, queue)
    login_monitor = LoginMonitor(COMPUTER_NAME)
    app_monitor = ApplicationMonitor(COMPUTER_NAME)
    heartbeat = Heartbeat(COMPUTER_NAME, location="Lab A")

    try:
        login_payload = login_monitor.detect_login("student01")
        api.post("/api/sessions/login", login_payload)
        print("Login event sent successfully.")
    except Exception as exc:
        print(f"Login send failed: {exc}")
        queue.add_event("sessions/login", login_monitor.detect_login("student01"))

    try:
        app_payload = app_monitor.record_activity("Google Chrome", "student01")
        api.post("/api/activities/application", app_payload)
        print("Application usage sent successfully.")
    except Exception as exc:
        print(f"Application send failed: {exc}")
        queue.add_event("activities/application", app_payload if 'app_payload' in locals() else app_monitor.record_activity("Google Chrome", "student01"))

    while True:
        try:
            payload = heartbeat.build_payload()
            api.post("/api/agents/heartbeat", payload)
            print("Heartbeat sent.")
            sync.sync_pending()
            time.sleep(30)
        except Exception as exc:
            print(f"Heartbeat failed: {exc}")
            queue.add_event("agents/heartbeat", heartbeat.build_payload())
            time.sleep(30)


if __name__ == "__main__":
    main()
