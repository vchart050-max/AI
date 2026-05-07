# PRD — vchart050-max/AI

## Original Problem Statement
> "this is my code https://github.com/vchart050-max/AI — i want to upload this on supabase but some code are written for mongodb tell me if thats true"
>
> Followed by: rewrite the backend so it works with Supabase (PostgreSQL) instead of MongoDB. Fresh start, no data migration needed.

## Architecture
- **Frontend:** React (unchanged — API contract preserved)
- **Backend:** FastAPI on port 8001 (supervisor-managed)
- **Database:** Supabase PostgreSQL via Transaction Pooler (port 6543)
- **ORM:** SQLAlchemy 2.x (async with asyncpg)
- **Migrations:** Alembic

## What's been implemented (May 7, 2026)
- Removed MongoDB / motor / pymongo from runtime path (env vars kept for backward compatibility per platform rules; not used).
- Added SQLAlchemy async engine (`backend/database.py`) configured for Supabase Transaction Pooler:
  - `statement_cache_size=0` (required by pooler)
  - `expire_on_commit=False`
  - Pool size 10 + 5 overflow
- Added `backend/models.py` with `StatusCheck` SQLAlchemy model.
- Rewrote `backend/server.py`:
  - `GET /api/` → "Hello World"
  - `POST /api/status` → inserts row into `status_checks` table
  - `GET /api/status` → returns all rows ordered by timestamp desc (limit 1000)
- Set up Alembic with sync URL and `Base.metadata` autogenerate (`backend/alembic/`).
- Generated and applied initial migration → `status_checks` table now exists in Supabase.
- Updated `backend/.env` with `DATABASE_URL` (Transaction Pooler URI, password URL-encoded).
- Updated `backend/requirements.txt` via `pip freeze` (sqlalchemy, asyncpg, alembic, psycopg2-binary added).
- End-to-end tested with `curl` via the public REACT_APP_BACKEND_URL — all 4 tests passed (root, two POSTs, GET).

## Core Requirements (static)
- Use Supabase PostgreSQL as primary DB.
- Frontend API contract unchanged (no React changes needed).
- Credentials loaded from `.env` only — easy to swap projects later.

## Backlog / Next Action Items
- **P1:** Build out actual app features (the codebase was a starter template; only `status_checks` exists). Decide on real domain models for the "AI" app.
- **P1:** Add indexes to columns used in WHERE/ORDER BY when real models are added.
- **P2:** Rotate the Supabase database password (it was shared in chat).
- **P2:** Disable RLS warnings or add policies if RLS is enabled later.
- **P2:** Add `.env.example` for documentation.
- **P3:** Consider Supabase Auth / Storage / Realtime if those features are needed.
- **P3:** Add unit tests for endpoints.

## Notes
- `MONGO_URL` and `DB_NAME` are kept in `.env` per platform protected-variables rule but are NOT used by the application anymore.
- Transaction Pooler URL is required (port 6543, host `*.pooler.supabase.com`); direct connection (port 5432) will NOT work without IPv4 add-on.
