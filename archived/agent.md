# agent.md — archived

**Retired code. Frozen history — do not extend.**

This directory holds the previous architecture of Urunan, before the app was
rewritten as the single self-contained `urunan.html` at the repo root. It is
kept for reference only.

## Contents

- `backend/` — the old FastAPI + SQLAlchemy + SQLite server.
- `frontend/` — the old Vue 3 + Vite + Tailwind + Auth0 single-page client.
- `docker-deploy.yml` — the old CI/CD workflow that built and pushed Docker
  images for the backend and frontend to GHCR and deployed over SSH.

## For agents

- **Do not add features here.** The live app is `urunan.html` at the repo root.
- Treat everything under `archived/` as read-only unless the user explicitly
  asks to revive or migrate from this stack.
- This code depends on services no longer in use (Auth0, a hosted DB, GHCR,
  an SSH deploy target) and is not wired into any current workflow.
