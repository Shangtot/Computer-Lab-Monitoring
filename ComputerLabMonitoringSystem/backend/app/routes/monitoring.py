from __future__ import annotations

import csv
import io
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..authentication.security import (create_access_token, get_authenticated_user,
                                       hash_password, require_admin, require_reader,
                                       verify_password)
from ..database import database_health_check, get_db
from ..models.db_models import Agent, ApplicationActivity, Computer, EventLog, StudentSession, User, WebsiteActivity
from ..schemas.schemas import (ApplicationEventRequest, HeartbeatRequest,
                               SessionEventRequest, UserLoginRequest,
                               WebsiteDomainRequest)
from ..utils.formatters import humanize_seconds, normalize_domain

router = APIRouter(prefix="/api")


def ensure_seed_data(db: Session) -> None:
    if db.query(User).count() == 0:
        db.add_all([
            User(username="admin", password_hash=hash_password("Admin123!"), role="admin"),
            User(username="viewer", password_hash=hash_password("Viewer123!"), role="viewer"),
        ])
        db.commit()

    if db.query(Agent).count() == 0:
        db.add(
            Agent(name="lab-agent", computer_name="PC-01", api_key="school-agent-key")
        )
        db.commit()


def get_or_create_computer(db: Session, computer_name: str, location: str | None = None) -> Computer:
    computer = db.query(Computer).filter(Computer.computer_name == computer_name).first()
    if computer is None:
        computer = Computer(computer_name=computer_name, location=location, is_online=True, last_heartbeat=datetime.utcnow())
        db.add(computer)
        db.commit()
        db.refresh(computer)
    return computer


@router.get("/health")
def health() -> dict:
    return {"status": "ok", "database": database_health_check()}


@router.post("/auth/login")
def login(payload: UserLoginRequest, db: Session = Depends(get_db)):
    ensure_seed_data(db)
    user = db.query(User).filter(User.username == payload.username).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(user.username, user.role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"username": user.username, "role": user.role}
    }


@router.get("/auth/me")
def me(current_user: User = Depends(get_authenticated_user)):
    return {"username": current_user.username, "role": current_user.role}


@router.get("/dashboard/summary")
def dashboard_summary(current_user: User = Depends(require_reader), db: Session = Depends(get_db)):
    ensure_seed_data(db)
    total_users = db.query(User).count()
    total_computers = db.query(Computer).count()
    active_sessions = db.query(StudentSession).filter(StudentSession.status == "active").count()
    online_computers = db.query(Computer).filter(Computer.is_online.is_(True)).count()
    total_app_usage = db.query(ApplicationActivity).count()
    total_web_domains = db.query(WebsiteActivity).count()
    return {
        "username": current_user.username,
        "role": current_user.role,
        "summary": {
            "total_users": total_users,
            "total_computers": total_computers,
            "active_sessions": active_sessions,
            "online_computers": online_computers,
            "total_app_usage": total_app_usage,
            "total_web_domains": total_web_domains,
        },
    }


@router.get("/computers")
def list_computers(current_user: User = Depends(require_reader), db: Session = Depends(get_db)):
    rows = db.query(Computer).order_by(Computer.computer_name).all()
    return [{
        "id": row.id,
        "computer_name": row.computer_name,
        "location": row.location,
        "is_online": row.is_online,
        "last_heartbeat": row.last_heartbeat.isoformat() if row.last_heartbeat else None,
    } for row in rows]


@router.get("/sessions")
def list_sessions(current_user: User = Depends(require_reader), db: Session = Depends(get_db)):
    rows = db.query(StudentSession).order_by(StudentSession.login_time.desc()).all()
    return [{
        "id": row.id,
        "computer_name": row.computer.computer_name if row.computer else None,
        "username": row.username,
        "login_time": row.login_time.isoformat(),
        "logout_time": row.logout_time.isoformat() if row.logout_time else None,
        "duration": humanize_seconds(row.session_duration_seconds),
        "status": row.status,
    } for row in rows]


@router.get("/applications")
def list_applications(current_user: User = Depends(require_reader), db: Session = Depends(get_db)):
    rows = db.query(ApplicationActivity).order_by(ApplicationActivity.start_time.desc()).all()
    return [{
        "id": row.id,
        "computer_name": row.computer_id,
        "app_name": row.app_name,
        "start_time": row.start_time.isoformat(),
        "end_time": row.end_time.isoformat() if row.end_time else None,
        "duration": humanize_seconds(row.duration_seconds),
    } for row in rows]


@router.get("/website-activity")
def website_activity(current_user: User = Depends(require_reader), db: Session = Depends(get_db)):
    rows = db.query(WebsiteActivity).order_by(WebsiteActivity.accessed_at.desc()).all()
    return [{
        "id": row.id,
        "domain": row.domain,
        "accessed_at": row.accessed_at.isoformat(),
    } for row in rows]


@router.post("/sessions/login")
def record_login(payload: SessionEventRequest, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    computer = get_or_create_computer(db, payload.computer_name)
    session = StudentSession(
        computer_id=computer.id,
        username=payload.username,
        login_time=payload.login_time or datetime.utcnow(),
        status=payload.status or "active",
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    db.add(EventLog(event_type="login", computer_id=computer.id, details=f"{payload.username} logged in"))
    db.commit()
    return {"success": True, "session_id": session.id}


@router.post("/sessions/logout")
def record_logout(payload: SessionEventRequest, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    computer = get_or_create_computer(db, payload.computer_name)
    session = db.query(StudentSession).filter(
        StudentSession.computer_id == computer.id,
        StudentSession.username == payload.username,
        StudentSession.status != "completed",
    ).order_by(StudentSession.login_time.desc()).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Active session not found")

    logout_time = payload.logout_time or datetime.utcnow()
    session.logout_time = logout_time
    session.status = "completed"
    session.session_duration_seconds = int((logout_time - session.login_time).total_seconds())
    db.add(EventLog(event_type="logout", computer_id=computer.id, details=f"{payload.username} logged out"))
    db.commit()
    return {"success": True, "session_id": session.id, "duration_seconds": session.session_duration_seconds}


@router.post("/activities/application")
def record_app_activity(payload: ApplicationEventRequest, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    computer = get_or_create_computer(db, payload.computer_name)
    session = db.query(StudentSession).filter(
        StudentSession.computer_id == computer.id,
        StudentSession.username == payload.username,
        StudentSession.status == "active",
    ).order_by(StudentSession.login_time.desc()).first()
    if session is None:
        raise HTTPException(status_code=404, detail="Active session not found for application activity")

    start_time = payload.start_time or datetime.utcnow()
    end_time = payload.end_time or datetime.utcnow()
    duration = payload.duration_seconds or int((end_time - start_time).total_seconds())
    activity = ApplicationActivity(
        computer_id=computer.id,
        session_id=session.id,
        app_name=payload.app_name,
        start_time=start_time,
        end_time=end_time,
        duration_seconds=duration,
    )
    db.add(activity)
    db.commit()
    return {"success": True, "app_name": payload.app_name, "duration_seconds": duration}


@router.post("/agents/heartbeat")
def heartbeat(payload: HeartbeatRequest, db: Session = Depends(get_db)):
    computer = get_or_create_computer(db, payload.computer_name, payload.location)
    computer.is_online = payload.status.lower() == "online"
    computer.last_heartbeat = datetime.utcnow()
    db.add(Agent(name=f"{payload.computer_name}-agent", computer_name=payload.computer_name, api_key=f"{payload.computer_name.lower()}-key"))
    db.add(EventLog(event_type="heartbeat", computer_id=computer.id, details=f"Status set to {payload.status}"))
    db.commit()
    return {"success": True, "computer_name": payload.computer_name, "status": payload.status}


@router.post("/website-domain")
def record_website_domain(payload: WebsiteDomainRequest, db: Session = Depends(get_db)):
    computer = get_or_create_computer(db, payload.computer_name)
    domain = normalize_domain(payload.domain)
    session = None
    if payload.session_id is not None:
        session = db.query(StudentSession).filter(StudentSession.id == payload.session_id).first()

    website = WebsiteActivity(
        computer_id=computer.id,
        session_id=session.id if session else None,
        domain=domain,
        accessed_at=datetime.utcnow(),
    )
    db.add(website)
    db.commit()
    return {"success": True, "domain": domain}


@router.get("/reports/export.csv")
def export_usage_report(current_user: User = Depends(require_reader), db: Session = Depends(get_db)):
    rows = db.query(WebsiteActivity).all()
    data = [{"domain": row.domain, "accessed_at": row.accessed_at.isoformat()} for row in rows]
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=["domain", "accessed_at"])
    writer.writeheader()
    writer.writerows(data)
    response = StreamingResponse(iter([csv_buffer.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=lab-usage-report.csv"
    return response
