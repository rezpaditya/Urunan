# agent.md — sync-server

The optional cross-device sync relay for Urunan.

## What it is

A tiny **stateless** rendezvous server that lets the app sync a trip between
devices. It is entirely optional — Urunan works fully offline without it, and
sync is off unless the app is pointed at a relay via `SYNC_BASE_URL`.

## Files

- `server.py` — The whole server. Python **standard library only**, one file.
  API:
  - `PUT /room/<id>` — store a payload for a room → `204`
  - `GET /room/<id>` — fetch the current payload → `200` | `404`
  - `GET /` — health check → `200`
  - `OPTIONS *` — CORS preflight → `204`
- `requirements.txt` — Dependencies (none needed at runtime; stdlib only).
- `Procfile` — Process definition for platforms like Heroku/Railway.
- `README.md` — Deploy steps and a curl-based smoke test.

## Design invariants — keep these true

- **Stores nothing durably.** Room payloads live only in memory and only for
  `TTL_SECONDS` (300s), then are evicted. A restart wipes everything. The
  devices' `localStorage` is the sole home of the data.
- **Can't read the data.** The client gzips and AES-GCM encrypts each payload
  before sending; the key never leaves the share link / the devices, so the
  relay only ever holds ciphertext. Never add code that would inspect,
  decrypt, log, or persist payload contents.
- **No dependencies.** Keep it standard-library-only and single-file.
- Room ids are validated against `ROOM_ID_RE` (22-char base64url) and bodies
  are capped at `MAX_BODY_BYTES`. Preserve these guards.

## Run locally

```bash
PORT=8080 python server.py
```
