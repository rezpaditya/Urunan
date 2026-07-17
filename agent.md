# agent.md — repository root

Guidance for AI agents working in the Urunan repository.

## What this project is

Urunan is a bill-splitting app for trips and group activities. The **entire
current app is a single self-contained file**, [`urunan.html`](urunan.html):
Vue 3 and a QR-code generator are inlined, styling is hand-written CSS, and
all data lives in the browser's `localStorage`. There is no server, no build
step, and no dependencies for the app itself.

Live app: https://rezpaditya.github.io/Urunan/

## Layout

| Path             | What it is                                                       |
| ---------------- | --------------------------------------------------------------- |
| `urunan.html`    | The whole app — the primary artifact of this repo.              |
| `sync-server/`   | Optional stateless relay for cross-device sync (Python stdlib). |
| `.github/`       | GitHub Actions — publishes `urunan.html` to GitHub Pages.       |
| `.vscode/`       | Editor launch configs (mostly for the archived stack).          |
| `archived/`      | The old FastAPI + Vue/Vite client. **Retired — do not extend.** |
| `README.md`      | User- and contributor-facing overview.                          |

## Working conventions

- **`urunan.html` is the app.** Feature work, bug fixes, and styling changes
  go here. Keep it self-contained: no external CDN links, no build tooling,
  no added runtime dependencies. Everything ships inlined.
- **Data lives in `localStorage`** per device. There is no backend database;
  don't introduce one.
- **Sync is optional and off by default.** It only activates when the app is
  pointed at a relay via `SYNC_BASE_URL` near the top of `urunan.html`. The
  relay never sees plaintext — payloads are gzipped and AES-GCM encrypted in
  the browser first. Keep that property intact.
- **`archived/` is frozen.** It documents the previous architecture; treat it
  as read-only history unless explicitly asked to revive it.
- Publishing to GitHub Pages happens automatically when `urunan.html` changes
  on `main` (see `.github/workflows/`). Don't hand-edit the `gh-pages` branch.

## Verifying changes

Open `urunan.html` directly in a browser (a `file://` URL works) and exercise
the affected flow. There is no test suite or build to run for the main app.
