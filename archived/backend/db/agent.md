# agent.md — archived/backend/db

**Retired.** Data layer for the old FastAPI backend. See `../../agent.md`.

## Files

- `database.py` — SQLAlchemy engine/session setup. Builds the SQLite URL from
  the `DB_FILE_PATH` env var, defines `SessionLocal` and the declarative
  `Base`, and seeds initial users via an `after_create` hook.
- `models.py` — ORM models: `User`, `Trip`, `Transaction`, `TransactionDetail`,
  and the `trip_user` association table (many-to-many trips↔users).
- `schemas.py` — Pydantic request/response schemas.
- `crud.py` — Generic DB helpers (`get`, `get_by_id`, `create`, …) that take a
  DAO/model class so they work across entities.

## Notes

- SQLite with `check_same_thread=False`; single-file DB.
- Frozen — do not modify. Current app uses browser `localStorage`, not a DB.
