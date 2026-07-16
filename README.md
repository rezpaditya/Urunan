# Urunan 🧾
### _Split your bills_

Urunan is a bill-splitting app for trips and group activities: create a trip,
invite participants, record who paid what, and see who owes whom. Settle the
trip when everyone is square.

**Live app: https://rezpaditya.github.io/Urunan/**

The entire app is a single self-contained file — [`urunan.html`](urunan.html).
No server, no build step, no dependencies: Vue 3 and a QR code generator are
inlined, styling is hand-written CSS, and all data lives in your browser's
localStorage.

## Using the app

- **On your phone:** open the live URL in Safari/Chrome, then *Share → Add to
  Home Screen* to get a full-screen app icon.
- **Offline / no hosting:** download `urunan.html` and open it in any browser.
  Everything works from a `file://` URL too.

### Features

- Trips with multiple participants
- Transactions with custom payment splits (defaults to an even split,
  adjustable per person, validated against the total)
- Automatic debt settlement summary — minimal set of "who pays whom"
- Share a trip between devices with a **link or QR code** — no server
  involved: the trip data travels inside the URL fragment and merges
  automatically on import (repeat imports never duplicate data)
- **Optional live device sync** — enable it on a trip and changes flow
  both ways automatically across your devices via a tiny relay you host
  (see below). Off by default; the app is fully usable without it.
- Works offline; data persists in localStorage per device

## Optional: cross-device sync backend

Sync is **off unless you point the app at a relay** and is disabled entirely
when `SYNC_BASE_URL` (near the top of `urunan.html`) is left empty — forks work
untouched. The relay is a stateless rendezvous, not a database:

- It **stores nothing**. Payloads sit in memory for a few minutes so the other
  device can pick them up, then are evicted. Your devices' localStorage stays
  the sole home of your data.
- It **can't read your data**. Each payload is gzipped and AES-GCM encrypted in
  the browser; the key lives only in the sync link, so the relay only ever sees
  ciphertext.
- It's one standard-library Python script — see
  [`sync-server/`](sync-server/) for the code and deploy steps.

Deploy to Google Cloud Run (free tier, needs a GCP project with billing
enabled), then paste the service URL into `SYNC_BASE_URL`:

```bash
cd sync-server
gcloud services enable run.googleapis.com
gcloud run deploy urunan-sync --source . --region <your-region> --allow-unauthenticated
```

**How it syncs:** enabling sync on a trip mints a random room id + encryption
key; other devices join by opening the `#sync=…` link or scanning its QR. Each
sync pulls the room, merges it locally, and pushes the merged result back, so
devices converge without duplicating anything.

**Limitations:** the relay only holds the most recent push per room, in memory —
if it restarts or scales to zero the room empties, but no data is lost because
each device re-seeds it on the next sync. Deleting an entire **trip** is
local-only and does not propagate (deleting a single transaction does, via
tombstones).

## Development

Edit `urunan.html`, open it in a browser, refresh. That's the whole loop.

## Deployment

Pushing a change to `urunan.html` on `main` triggers the
[`github-pages`](.github/workflows/github-pages.yml) workflow, which copies it
to the `gh-pages` branch as `index.html`; GitHub Pages publishes from there.
Manual alternative: commit the file to `gh-pages` yourself.

## Archived

The original implementation — a Vue 3 + Vite SPA with a FastAPI/SQLAlchemy
backend, Auth0 authentication, and Docker-based deployment — lives in
[`archived/`](archived/) for reference. It is no longer deployed or maintained.
