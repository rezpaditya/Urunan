# agent.md — repository root

Guidance for AI agents working in the Urunan repository.

## What this project is

Urunan is a bill-splitting app for trips and group activities. The **entire
current app is a single self-contained file**, [`urunan.html`](urunan.html):
Vue 3 and a QR-code generator are inlined, styling is hand-written CSS, and
all data lives in the browser's `localStorage`. There is no build step and no
bundled dependencies for the app itself. Cross-device sync is an **optional**
layer over Cloud Firestore that only activates when a Firebase config is
present (see `FIREBASE_SETUP.md`); with it blank the app is fully local.

Live app: https://rezpaditya.github.io/Urunan/

## Layout

| Path             | What it is                                                       |
| ---------------- | --------------------------------------------------------------- |
| `urunan.html`       | The whole app — the primary artifact of this repo.              |
| `FIREBASE_SETUP.md` | How to wire up optional Cloud Firestore sync (config + rules).  |
| `tests/`            | Playwright smoke tests (one spec per mandatory feature).        |
| `.github/`          | GitHub Actions — publishes `urunan.html` to GitHub Pages.       |
| `.vscode/`          | Editor launch configs (mostly for the archived stack).          |
| `archived/`         | The old FastAPI + Vue/Vite client. **Retired — do not extend.** |
| `README.md`         | User- and contributor-facing overview.                          |

## Working conventions

- **`urunan.html` is the app.** Feature work, bug fixes, and styling changes
  go here. Keep it self-contained: Vue, the QR generator, CSS, and app logic
  all ship inlined with no build tooling. The one sanctioned network
  dependency is the Firebase SDK, lazily imported from the CDN *only* when
  cloud sync is configured — don't add other CDN links or bundlers.
- **`localStorage` is the source of truth**, per device, so the app stays
  offline-first. Firestore is a sync layer on top, never a hard dependency:
  code must keep working when a config is blank or the SDK can't load.
- **Sync is optional and off by default.** It only activates when
  `FIREBASE_CONFIG` (near the top of `urunan.html`) is filled in. Trips are
  mirrored to Cloud Firestore under an unguessable doc id shared via the
  `#fs=<id>` link; devices converge through the `mergeTrip()` CRDT. Preserve
  the offline-first degradation and keep the security model documented in
  `FIREBASE_SETUP.md` in sync with any rule changes.
- **`archived/` is frozen.** It documents the previous architecture; treat it
  as read-only history unless explicitly asked to revive it.
- Publishing to GitHub Pages happens automatically when `urunan.html` changes
  on `main` (see `.github/workflows/`). Don't hand-edit the `gh-pages` branch.

## Verifying changes

Open `urunan.html` directly in a browser (a `file://` URL works) and exercise
the affected flow. There is also a Playwright smoke suite covering the
mandatory features — run it with `cd tests && npm install && npx playwright
test`. The suite runs with sync disabled (blank config), so it must stay green
regardless of Firebase.
