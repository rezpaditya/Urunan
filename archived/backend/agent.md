# agent.md — archived/backend

**Retired.** The old FastAPI backend for Urunan. Not used by the current app
(`urunan.html`). Kept for reference only — see `../agent.md`.

## What it was

A FastAPI service backed by SQLAlchemy over SQLite. It exposed REST endpoints
for trips, transactions, and users.

## Layout

- `main.py` — App entrypoint. Creates FastAPI, adds permissive CORS, seeds the
  user table on create, and mounts the routers.
- `dependency.py` — `get_db` dependency yielding a SQLAlchemy session.
- `db/` — SQLAlchemy models, schemas (Pydantic), CRUD helpers, engine/session.
- `router/` — API routers: `trips`, `transactions`, `users`.
- `Dockerfile`, `Pipfile`, `Pipfile.lock` — container build and deps.
- `cert.pem`, `key.pem` — TLS material for the old deployment.
- `__ini__.py` — (note the typo) an old package marker.

## Notes for agents

- Runtime config came from env: `DB_FILE_PATH` sets the SQLite path (see
  `db/database.py`).
- CORS was wide open (`allow_origins=["*"]`) — a known rough edge of this
  retired stack, not a pattern to copy.
- Do not extend this. New work belongs in `urunan.html`.
