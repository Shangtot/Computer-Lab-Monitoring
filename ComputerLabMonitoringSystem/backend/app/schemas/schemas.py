from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserLoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=80)
    password: str = Field(..., min_length=4)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class HeartbeatRequest(BaseModel):
    computer_name: str
    status: str = "online"
    location: Optional[str] = None


class SessionEventRequest(BaseModel):
    computer_name: str
    username: str
    login_time: Optional[datetime] = None
    logout_time: Optional[datetime] = None
    session_duration_seconds: Optional[int] = None
    status: str = "active"


class ApplicationEventRequest(BaseModel):
    computer_name: str
    username: str
    app_name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_seconds: Optional[int] = None


class WebsiteDomainRequest(BaseModel):
    computer_name: str
    domain: str
    session_id: Optional[int] = None


class DashboardSummary(BaseModel):
    total_users: int
    total_computers: int
    active_sessions: int
    online_computers: int
    total_app_usage: int
    total_web_domains: int
