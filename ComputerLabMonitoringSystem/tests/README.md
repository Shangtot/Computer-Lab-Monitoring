# Test plan

This folder contains a minimal verification suite for the FastAPI backend and monitoring agent logic.

## Run tests

```bash
pytest -q
```

## Expected checks

- Root endpoint is reachable.
- Admin login succeeds with the seeded test credentials.
- Basic API routes return data without crashing.
