# Network design and testing notes

## Overview

The monitoring system is designed as a centralized architecture. Multiple laboratory computers connect to a central server on the same LAN or VLAN. The central server exposes the FastAPI backend over HTTPS in production and the lab computers run a Python monitoring agent that emits events to the server.

## Suggested Packet Tracer design

- 1 central switch
- 3 lab computers: PC-01, PC-02, PC-03
- 1 server acting as the application and database host
- Optional firewall and router for internet access separation
- One management workstation used by staff for dashboard access

## Communication flow

1. Each lab computer runs the Python agent.
2. The agent collects login, logout, application, and heartbeat events.
3. When the backend is reachable, the agent posts JSON payloads over HTTPS.
4. If the server is unavailable, the agent writes data to SQLite and syncs later.
5. The central server persists data into MySQL or SQLite fallback.

## Wireshark usage

- Capture traffic between the server and a test computer.
- Verify the HTTPS handshake and JSON payload size.
- Check for duplicate submissions and failed connections.
- Inspect heartbeat timings and delay spikes.

## Production notes

- Use TLS certificates and configure reverse proxy termination.
- Separate the management network from student lab traffic where possible.
- Restrict ports to the monitoring service and database.
