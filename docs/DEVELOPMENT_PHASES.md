# Development phases

## Phase 1: Project setup and environment

Objectives:
- Prepare the project directory and VS Code workspace.
- Configure Python and dependency management.
- Prepare local database and environment variables.

Tasks:
- Create the project structure.
- Install Python dependencies.
- Configure `.env` files.
- Validate the environment.

Expected result:
The project is ready for backend and agent development.

## Phase 2: Database design and setup

Objectives:
- Define MySQL-ready tables for users, computers, sessions, applications, and domains.
- Prepare SQLite fallback for local desktop testing.

Tasks:
- Create schema.sql.
- Seed known admin and viewer users.
- Add indexes for common reports.

Expected result:
The system has a working persistent structure for data collection.

## Phase 3: Backend API development

Objectives:
- Build the FastAPI server.
- Implement authentication and validation.
- Expose API endpoints for monitoring logs.

Tasks:
- Implement database connection logic.
- Create routes for auth, sessions, apps, heartbeats, and reports.
- Validate input payloads.

Expected result:
The backend can receive and store monitoring events.

## Phase 4: First working slice

Objectives:
- Start with one lab computer.
- Send a valid login event to the central server.

Tasks:
- Start the backend.
- Send a login event through the agent.
- Verify the record in the dashboard.

Expected result:
A single lab computer successfully sends authentication data to the backend.

## Phase 5: Core computer monitoring

Objectives:
- Track login/logout lifecycle.
- Monitor application usage and durations.
- Detect unexpected computer shutdowns.

Expected result:
The system can record core lab activity with accurate timing.

## Phase 6: Offline event storage and synchronization

Objectives:
- Queue records locally when the server is unavailable.
- Retry connectivity automatically.

Expected result:
Monitoring continues when the network is interrupted.

## Phase 7: Website monitoring

Objectives:
- Capture hostnames only from managed browsers.
- Send those domains to the monitoring agent.

Expected result:
The system records approved website domains without collecting personal content.

## Phase 8: Admin dashboard development

Objectives:
- Build HTML/CSS/JS dashboard pages.
- Connect static pages to the API.

Expected result:
Staff can view live activity and filters.

## Phase 9: Authentication and access control

Objectives:
- Separate admin and viewer access.
- Protect API and dashboard routes.

Expected result:
Only authorized users can see or alter protected content.

## Phase 10: Reports and analytics

Objectives:
- Support CSV/PDF and printable reports.
- Filter by date, computer, and student.

Expected result:
Staff can generate operational and usage reports.

## Phase 11: Network design and integration

Objectives:
- Document LAN design and server placement.
- Simulate the network in Cisco Packet Tracer.

Expected result:
The communication design is documented and verifiable.

## Phase 12: Testing and debugging

Objectives:
- Validate login capture, logout capture, heartbeat flow, and API operations.
- Confirm dashboard readability and data integrity.

Expected result:
The project is ready for pilot deployment in a small lab environment.
