# Installation guide

## Requirements

- Python 3.11+
- MySQL Server 8.0+
- VS Code on Windows
- Optional: Cisco Packet Tracer and Wireshark for network validation

## Environment setup

1. Create a Python virtual environment.
2. Install project dependencies from the root `requirements.txt` and backend/agent requirements files.
3. Copy `.env.example` and `backend/.env.example` to `.env` and `backend/.env`.
4. Set database credentials and secret values before starting the service.

## Start backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Start agent

```bash
python agent/main.py
```

## Access dashboard

Open `frontend/login.html` in the browser or serve the folder using a local static server.
