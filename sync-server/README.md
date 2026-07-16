# Urunan sync relay

A tiny **stateless** rendezvous server that lets Urunan sync a trip between
your devices. It is optional — Urunan works fully offline without it.

## What it does (and doesn't)

- Devices `PUT` an encrypted trip payload to a random room id and `GET` the
  latest payload for that room. That's the whole API.
- **It stores nothing.** Payloads live only in memory, only for a few minutes
  (`TTL_SECONDS`), then are evicted. Restarting the process wipes everything.
  Your devices' `localStorage` remains the sole home of your data.
- **It can't read your data.** The client gzips and AES-GCM encrypts each
  payload before sending; the encryption key never leaves the share link /
  your devices, so the relay only ever holds ciphertext.
- Standard library only — no `pip install`, one file: [`server.py`](server.py).

## Run locally

```bash
PORT=8080 python server.py
```

Quick check:

```bash
curl -s localhost:8080/                         # {"status":"ok"}
ID=AAAAAAAAAAAAAAAAAAAAAA                         # 22-char base64url
curl -s -X PUT --data-binary 'hello' localhost:8080/room/$ID   # 204
curl -s localhost:8080/room/$ID                  # hello
```

Then point the app at it: set `SYNC_BASE_URL = 'http://localhost:8080'` near
the top of `urunan.html`.

## Deploy to Google Cloud Run

Requires a GCP project with billing enabled (Cloud Run has a free tier).

```bash
gcloud services enable run.googleapis.com

gcloud run deploy urunan-sync \
  --source . \
  --region <your-region> \
  --allow-unauthenticated
#   add --min-instances=1 to keep the relay always warm (small cost);
#   the default (scale to zero) is free but empties the in-memory rooms
#   after the instance idles — harmless, devices re-seed on the next sync.
```

Cloud Run builds straight from this directory (via the `Procfile` — no
Dockerfile needed) and prints a service URL. Paste that URL into
`SYNC_BASE_URL` in `urunan.html`, commit, and the GitHub Pages deploy picks
it up.

## Limitations

- The relay only holds the **most recent** push per room, in memory. Two
  devices sync by each pushing their merged trip and pulling the other's;
  a push that lands between another device's pull and push is not lost —
  it reappears on that device's next sync (the client merge is a union).
- If the instance restarts or scales to zero, in-flight rooms vanish. No data
  is lost because every device keeps the full trip and re-seeds the room the
  next time it syncs.
- Deleting an entire **trip** is local-only and does not propagate.
