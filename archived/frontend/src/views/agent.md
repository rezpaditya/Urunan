# agent.md — archived/frontend/src/views

**Retired.** Route-level pages for the old Vue client. See `../agent.md`.

## Files

- `Home.vue` — Landing page; handles Auth0 login and redirects.
- `Trip.vue` — Trip list / create.
- `TripDetail.vue` — Single trip, its participants and transactions.
- `Transaction.vue` — Transaction list / create.
- `TransactionDetail.vue` — Single transaction with per-person split.

## Notes

- Wired to routes in `../router/index.js`; some routes are Auth0-guarded.
- Frozen — reference only.
