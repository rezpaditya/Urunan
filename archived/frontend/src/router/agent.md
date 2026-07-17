# agent.md — archived/frontend/src/router

**Retired.** Vue Router config for the old client. See `../agent.md`.

## Files

- `index.js` — Defines the router using `createWebHashHistory` and maps routes
  to the pages in `../views/` (home, trip, trip/:id, transaction,
  transaction/:id). Protected routes use Auth0's `authGuard` via `beforeEnter`.

## Notes

- Hash history is used so the SPA works on static hosting without server
  rewrites.
- Frozen — reference only.
