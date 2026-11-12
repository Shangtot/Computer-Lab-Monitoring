from __future__ import annotations

import csv
import io
from typing import Iterable

from sqlalchemy.orm import Session

from ..models.db_models import ApplicationActivity, StudentSession, WebsiteActivity


def get_dashboard_summary(db: Session) -> dict:
    total_users = db.query(db.query().from_statement('SELECT COUNT(*) FROM users').count())
    active_sessions = db.query(StudentSession).filter(StudentSession.status == "active").count()
    total_app_usage = db.query(ApplicationActivity).count()
    total_web_domains = db.query(WebsiteActivity).count()
    return {
        "total_users": total_users,
        "active_sessions": active_sessions,
        "total_app_usage": total_app_usage,
        "total_web_domains": total_web_domains,
    }


def export_csv(rows: Iterable[dict]) -> str:
    output = io.StringIO()
    fieldnames = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return output.getvalue()
