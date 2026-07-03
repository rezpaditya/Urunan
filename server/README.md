# Urunan sync relay

A ~80-line FastAPI WebSocket relay that lets Urunan devices sync live
**without storing anything**. Devices join a room named by an unguessable
`syncId` and the server forwards frames between currently-connected peers.
There is no database, no disk, no persistence: if nobody else is in the
room, frames go nowhere.

## Security model

- The `syncId` is a random 128-bit capability token generated in the
  browser — knowing it lets you join the room, nothing more.
- All payloads are end-to-end encrypted (AES-GCM-256) in the browser.
  The key travels only in the share URL's `#fragment`, which is never
  sent to any server. This relay only ever sees ciphertext.
- A hostile room member could send garbage frames, but AES-GCM
  authentication makes clients reject anything not encrypted with the
  real key. Every device keeps its full local copy regardless.
- Optional `ALLOWED_ORIGINS` (comma-separated) rejects WebSocket
  connections from other web origins as cheap abuse hardening.

## Local development

```bash
pip install -r requirements.txt
uvicorn main:app --port 8080
```

Smoke test the relay with two terminals:

```bash
python -m websockets ws://localhost:8080/v1/ws/AAAAAAAAAAAAAAAAAAAAAA
```

Anything typed in one terminal appears in the other; each also receives
`{"t": "peers", "n": ...}` presence updates from the server.

## Deploy to Google Cloud Run

```bash
gcloud run deploy urunan-sync --source . --region <region> \
  --allow-unauthenticated --max-instances 1 --memory 256Mi \
  --timeout 3600 \
  --set-env-vars ALLOWED_ORIGINS=https://rezpaditya.github.io
```

Then set `SYNC_API` in `urunan.html` to `wss://<the-run-url-without-https://>`
(i.e. replace the `https://` scheme with `wss://`).

Notes:

- **`--max-instances 1` is required.** Rooms live in process memory;
  two instances would split a room and peers would never see each other.
- `--timeout 3600` is Cloud Run's maximum WebSocket connection lifetime
  (1 h). Clients reconnect automatically when a connection is cut.
- WebSocket time counts as billable instance time. The client closes
  its sockets whenever the tab is hidden, so idle cost stays near zero.
