
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(
        String(80), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="admin", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class LabRoom(Base):
    __tablename__ = "lab_rooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    room_name: Mapped[str] = mapped_column(
        String(80), unique=True, nullable=False
    )
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    computers: Mapped[list["Computer"]] = relationship(back_populates="lab_room")


class Computer(Base):
    __tablename__ = "computers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    computer_name: Mapped[str] = mapped_column(
        String(80), unique=True, index=True, nullable=False
    )
    lab_room_id: Mapped[int | None] = mapped_column(
        ForeignKey("lab_rooms.id"), nullable=True
    )
    is_online: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_heartbeat: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    lab_room: Mapped[LabRoom | None] = relationship(back_populates="computers")
    agent: Mapped["Agent | None"] = relationship(
        back_populates="computer", uselist=False
    )
    sessions: Mapped[list["StudentSession"]] = relationship(
        back_populates="computer"
    )
    heartbeats: Mapped[list["Heartbeat"]] = relationship(
        back_populates="computer"
    )
    application_activities: Mapped[list["ApplicationActivity"]] = relationship(
        back_populates="computer"
    )
    website_activities: Mapped[list["WebsiteActivity"]] = relationship(
        back_populates="computer"
    )
    events: Mapped[list["EventLog"]] = relationship(back_populates="computer")


class Agent(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    computer_id: Mapped[int] = mapped_column(
        ForeignKey("computers.id"), unique=True, nullable=False
    )
    api_key_hash: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    last_seen: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    computer: Mapped[Computer] = relationship(back_populates="agent")


class StudentSession(Base):
    __tablename__ = "student_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    computer_id: Mapped[int] = mapped_column(
        ForeignKey("computers.id"), nullable=False
    )
    username: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    login_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    logout_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    session_duration_minutes: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), default="active", nullable=False)

    computer: Mapped[Computer] = relationship(back_populates="sessions")
    application_activities: Mapped[list["ApplicationActivity"]] = relationship(
        back_populates="session"
    )
    website_activities: Mapped[list["WebsiteActivity"]] = relationship(
        back_populates="session"
    )


class ApplicationActivity(Base):
    __tablename__ = "application_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    computer_id: Mapped[int] = mapped_column(
        ForeignKey("computers.id"), nullable=False
    )
    session_id: Mapped[int | None] = mapped_column(
        ForeignKey("student_sessions.id"), nullable=True
    )
    app_name: Mapped[str] = mapped_column(String(120), nullable=False)
    start_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    computer: Mapped[Computer] = relationship(back_populates="application_activities")
    session: Mapped[StudentSession | None] = relationship(
        back_populates="application_activities"
    )


class WebsiteActivity(Base):
    __tablename__ = "website_activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    computer_id: Mapped[int] = mapped_column(
        ForeignKey("computers.id"), nullable=False
    )
    session_id: Mapped[int | None] = mapped_column(
        ForeignKey("student_sessions.id"), nullable=True
    )
    domain: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    accessed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    computer: Mapped[Computer] = relationship(back_populates="website_activities")
    session: Mapped[StudentSession | None] = relationship(
        back_populates="website_activities"
    )


class Heartbeat(Base):
    __tablename__ = "heartbeats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    computer_id: Mapped[int] = mapped_column(
        ForeignKey("computers.id"), nullable=False
    )
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    status: Mapped[str] = mapped_column(String(20), default="online", nullable=False)

    computer: Mapped[Computer] = relationship(back_populates="heartbeats")


class EventLog(Base):
    __tablename__ = "event_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_type: Mapped[str] = mapped_column(String(50), nullable=False)
    computer_id: Mapped[int | None] = mapped_column(
        ForeignKey("computers.id"), nullable=True
    )
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )

    computer: Mapped[Computer | None] = relationship(back_populates="events")
