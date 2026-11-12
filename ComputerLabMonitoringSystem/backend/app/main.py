from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .authentication.security import hash_password
from .database import SessionLocal, init_db
from .models.db_models import Agent, User
from .routes.monitoring import router

app = FastAPI(title="Computer Lab Monitoring API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def seed_default_data() -> None:
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            db.add_all([
                User(username="admin", password_hash=hash_password("Admin123!"), role="admin"),
                User(username="viewer", password_hash=hash_password("Viewer123!"), role="viewer"),
            ])
        if db.query(Agent).count() == 0:
            db.add(Agent(name="lab-agent", computer_name="PC-01", api_key="school-agent-key"))
        db.commit()
    finally:
        db.close()


init_db()
seed_default_data()
app.include_router(router)


@app.get("/")
def read_root() -> dict:
    return {"app": "Computer Lab Monitoring System", "status": "online"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
