# agent.md — archived/frontend/src

**Retired.** Source of the old Vue 3 client. See `../agent.md`.

## Layout

- `main.js` — App bootstrap: creates the Vue app, installs Pinia, the router,
  and the Auth0 plugin, then mounts.
- `App.vue` — Root component.
- `router/` — Vue Router config (hash history, route guards via Auth0).
- `stores/` — Pinia stores (e.g. `user`).
- `views/` — Route-level pages (Home, Trip, TripDetail, Transaction,
  TransactionDetail).
- `components/` — Reusable UI pieces (`TripItem`, `TransactionItem`).
- `assets/` — Bundled assets imported by components.
- `index.css` / `style.css` — global styles (Tailwind layers + custom CSS).

## Notes

- Vue 3 `<script setup>` SFC style throughout.
- Frozen — do not extend. New work belongs in the root `urunan.html`.
