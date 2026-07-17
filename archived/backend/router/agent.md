# agent.md — archived/backend/router

**Retired.** FastAPI API routers for the old backend. See `../../agent.md`.

## Files

- `trips.py` — `/trips` endpoints (list, get by id, create, …).
- `transactions.py` — `/transactions` endpoints.
- `users.py` — `/users` endpoints.

## Pattern (for reference)

Each module defines an `APIRouter` with a `prefix` and `tags`, depends on
`get_db` from `../dependency.py`, and delegates persistence to the generic
helpers in `../db/crud.py` using the models from `../db/models.py`.

## Notes

- Frozen — do not extend. Mounted in `../main.py` via `include_router`.
