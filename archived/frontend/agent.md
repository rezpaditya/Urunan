# agent.md — archived/frontend

**Retired.** The old Vue 3 single-page client for Urunan. Not used by the
current app (`urunan.html`). Kept for reference only — see `../agent.md`.

## What it was

A Vue 3 (`<script setup>` SFCs) app built with Vite, styled with Tailwind CSS,
using Pinia for state, Vue Router for routing, `vue-multiselect` for inputs,
and Auth0 (`@auth0/auth0-vue`) for authentication. It talked to the FastAPI
backend under `../backend`.

## Layout

- `src/` — application source (see `src/agent.md`).
- `public/` — static assets served as-is.
- `index.html` — Vite HTML entry.
- `package.json` / `package-lock.json` — deps and scripts (`dev`, `build`,
  `preview`).
- `vite.config.js`, `postcss.config.js`, `tailwind.config.js` — build/styling.
- `.env` — environment config (Auth0 domain/client id, API base, etc.).
- `Dockerfile` — container build for the old deployment.
- `.vscode/` — recommended extensions.

## Notes for agents

- Frozen — do not extend. New work belongs in the root `urunan.html`.
- If ever run for reference: `npm install` then `npm run dev`. Depends on Auth0
  and the backend, which are no longer operated.
