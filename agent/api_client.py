from __future__ import annotations

import json
from typing import Any

import requests

from .config import API_KEY, BACKEND_URL


class ApiClient:
    def __init__(self, base_url: str = BACKEND_URL, api_key: str = API_KEY):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        headers = {"Content-Type": "application/json", "X-API-Key": self.api_key}
        response = requests.post(f"{self.base_url}{path}", json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def get(self, path: str) -> dict[str, Any]:
        response = requests.get(f"{self.base_url}{path}", headers={"X-API-Key": self.api_key}, timeout=10)
        response.raise_for_status()
        return response.json()
