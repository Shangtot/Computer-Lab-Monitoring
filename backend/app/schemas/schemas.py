
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


# ==============================
# ADMINISTRATOR AUTHENTICATION
# ==============================

class UserLoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=80)
    password: str = Field(..., min_length=4)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


# ==============================
# LABORATORY ROOM MANAGEMENT
# ==============================

class LabRoomCreateRequest(BaseModel):
    room_name: str = Field(..., min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=255)


class LabRoomUpdateRequest(BaseModel):
    room_name: str | None = Field(default=None, min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool | None = None


# ==============================
# COMPUTER MANAGEMENT
# ==============================

class ComputerCreateRequest(BaseModel):
    computer_name: str = Field(..., min_length=1, max_length=80)
    lab_room_id: int = Field(..., gt=0)


class ComputerUpdateRequest(BaseModel):
    lab_room_id: int | None = Field(default=None, gt=0)


# ==============================
# AGENT REGISTRATION
# ==============================

class AgentCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=80)
    computer_id: int = Field(..., gt=0)


class AgentCredentialResponse(BaseModel):
    agent_id: int
    computer_id: int
    api_key: str


# ==============================
# AGENT HEARTBEAT
# ==============================

class HeartbeatRequest(BaseModel):
    computer_name: str = Field(..., min_length=1, max_length=80)
    status: Literal["online"] = "online"


# ==============================
# STUDENT SESSIONS
# ==============================

class SessionEventRequest(BaseModel):
    computer_name: str = Field(..., min_length=1, max_length=80)
    username: str = Field(..., min_length=1, max_length=80)
    login_time: datetime | None = None
    logout_time: datetime | None = None
    session_duration_minutes: int | None = Field(default=None, ge=0)
    status: Literal["active", "completed"] = "active"


# ==============================
# APPLICATION MONITORING
# ==============================

class ApplicationEventRequest(BaseModel):
    computer_name: str = Field(..., min_length=1, max_length=80)
    username: str = Field(..., min_length=1, max_length=80)
    app_name: str = Field(..., min_length=1, max_length=120)
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_minutes: int | None = Field(default=None, ge=0)


# ==============================
# WEBSITE DOMAIN MONITORING
# ==============================

class WebsiteDomainRequest(BaseModel):
    computer_name: str = Field(..., min_length=1, max_length=80)
    domain: str = Field(..., min_length=1, max_length=150)
    session_id: int | None = Field(default=None, gt=0)


# ==============================
# DASHBOARD SUMMARY
# ==============================

class DashboardSummary(BaseModel):
    total_users: int
    total_computers: int
    active_sessions: int
    online_computers: int
    total_app_usage: int
    total_web_domains: int
