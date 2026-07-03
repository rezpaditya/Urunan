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
- Optional **live sync** through a zero-storage relay (see below): shared
  trips update across devices in real time while both are online
- Works offline; data persists in localStorage per device

## Live sync (optional)

Deploying the tiny WebSocket relay in [`server/`](server/) upgrades sharing:
the share link becomes a short `#join=` URL (always QR-friendly), and once a
friend has joined a trip, changes flow between devices automatically whenever
you're online at the same time. The relay **stores nothing** — it only
forwards end-to-end-encrypted snapshots between connected devices, so trip
data still lives exclusively in each participant's browser. The AES key
travels only in the share link's `#fragment`, which never reaches any server.

See [`server/README.md`](server/README.md) for deployment (Google Cloud Run)
and how to point the app at your relay. Without a relay configured, sharing
falls back to the classic self-contained `#trip=` link, which also remains
the fallback whenever the other person can't be online at the same time.

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
