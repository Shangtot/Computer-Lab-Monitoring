from __future__ import annotations

from .api_client import ApiClient
from .local_queue import LocalQueue


class SyncManager:
    def __init__(self, api_client: ApiClient, queue: LocalQueue):
        self.api_client = api_client
        self.queue = queue

    def sync_pending(self) -> list[dict]:
        results = []
        for event in self.queue.pending_events():
            try:
                self.api_client.post(f"/api/{event['event_type']}", event['payload'])
                self.queue.mark_sent(event['id'])
                results.append({"id": event['id'], "status": "sent"})
            except Exception:
                results.append({"id": event['id'], "status": "retry-later"})
        return results
