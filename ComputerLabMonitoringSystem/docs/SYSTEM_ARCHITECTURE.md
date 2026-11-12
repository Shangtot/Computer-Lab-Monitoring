# System architecture

## Overview

The system is built around three connected layers:

1. Agent layer – installed on each lab computer.
2. Backend layer – centralized FastAPI service for processing and storage.
3. Frontend layer – web dashboard with separate admin/viewer roles.

## Data flow

- A lab computer starts a local monitoring agent.
- The agent detects login/logout events and collects application usage data.
- Heartbeats report connectivity every 30–60 seconds.
- Website domain activity is captured by the browser extension and relayed to the agent.
- The agent submits records to the backend through HTTPS.
- The backend validates the payload, persists it to the database, and exposes reporting endpoints.
- Staff users authenticate to the dashboard and query reports.

## Storage strategy

- MySQL is the target production database for centralized records.
- SQLite is used as a local queue and fallback database for offline conditions.
- A retention policy can be configured to prune records after a set number of days.
