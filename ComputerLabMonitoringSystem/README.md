# Computer Lab Monitoring System

This project implements a centralized student computer activity monitoring and digital logbook system for school laboratories. It includes a Python monitoring agent, a FastAPI backend, a static web dashboard, a browser extension for website domain tracking, and supporting database, network, and documentation assets.

## Project goals

- Monitor lab computer login/logout events
- Track application usage and session durations
- Record website domains visited on managed browsers
- Store records centrally with MySQL-ready schema and SQLite fallback for local development
- Provide a role-based dashboard for administrators and viewers
- Support offline event queuing and automatic synchronization

## Main folders

- `backend/` – FastAPI API, database configuration, authentication, routes, and services
- `agent/` – local monitoring agent for each lab computer
- `browser-extension/` – managed browser extension for domain capture
- `frontend/` – dashboard pages and JavaScript front-end
- `database/` – schema and seed scripts
- `docs/` – architecture and deployment documentation
- `tests/` – automated verification tests

## Quick start

1. Copy environment files:
   - `cp .env.example .env`
   - `cp backend/.env.example backend/.env`
2. Create a Python virtual environment and install dependencies:
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
   - `pip install -r requirements.txt`
   - `pip install -r backend/requirements.txt`
   - `pip install -r agent/requirements.txt`
3. Initialize the database:
   - `python -c "from backend.app.database import init_db; init_db()"`
4. Start the backend:
   - `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
5. Open the front end:
   - `frontend/login.html` in a browser or serve via a static file server
6. Start a sample agent:
   - `python agent/main.py`

## Security notes

- Secrets are stored via environment variables.
- Browser activity only records domains, never full page content.
- The browser extension is designed for school-managed environments only.
- Data retention can be configured through environment settings.

## Documentation

See the files in `docs/` for architecture, installation, and phase-based development guidance.
