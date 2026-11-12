# Database design

## Tables

- `users` – staff account metadata and role assignments.
- `computers` – physical lab workstation metadata.
- `student_sessions` – login and logout lifecycle records.
- `application_activities` – process or app usage logs.
- `website_activities` – domains accessed by the managed browser.
- `heartbeats` – periodic connection status checks.
- `event_log` – general event traces for debugging.

## Relationship highlights

- Each session belongs to a specific computer.
- Applications and website records are associated with a computer and session.
- Staff users are separate from student activity records.
- Unique indexes help with searches by username and computer name.

## Retention

Set `RETENTION_DAYS` in the environment to automatically clean stale event data in production workloads.
