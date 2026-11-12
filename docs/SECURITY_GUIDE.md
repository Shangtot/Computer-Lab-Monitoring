# Security and privacy guide

## Authentication and authorization

- Dashboard access is protected using JWT tokens.
- Role checks deny non-admin writes to the monitoring endpoints.
- Research data and system operations are only available to staff accounts.

## Data minimalism

- The browser extension records only the hostname.
- No keystrokes, personal files, page contents, or screenshots are collected.
- The system can be configured with a retention period using `RETENTION_DAYS`.

## Deployment guidance

- Use HTTPS in production.
- Store database credentials in environment variables.
- Never expose secret keys in frontend JavaScript.
- Keep lab devices approved and monitored by school IT staff.
