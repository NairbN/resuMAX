# resuMAX

## Local Development (scripts)

### Prereqs
- Python 3.10+ (venv is auto-created by scripts)
- Node 18+ with pnpm
- Docker (for Postgres/Redis when using `make dev` or compose)

### Quick start (backend + frontend + db/redis)
```
make setup          # install backend/frontend deps
make dev            # starts dockerized db/redis, backend (uvicorn --reload), frontend (next dev)
```
- Ctrl+C stops backend/frontend and brings down db/redis.
- Backend env regenerates each run with a fresh `AUTH_SECRET`; frontend `.env.local` is regenerated and mock is off for `make dev`.

### Run individually (scripts/Make targets)
- Backend only (regens .env, uses Postgres if available else sqlite): `make backend`
- Frontend only (regens .env.local, mock on): `make frontend`
- Tests: `make test-backend`, `make test-frontend`, or `make test` for both.

## Docker

Build images once:
```
make docker-build
```

Run stack (db, redis, api, frontend) from images:
```
make docker-up
```
- Ctrl+C stops containers and runs `docker compose down`.
- Frontend builds with `NEXT_PUBLIC_USE_AUTH_MOCK=false` by default.

## Manual setup (optional)

Backend:
```
cd apps/api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # set DATABASE_URL, AUTH_SECRET, etc.
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

Frontend:
```
cd apps/frontend
pnpm install
cp .env.local.example .env.local  # set NEXT_PUBLIC_API_BASE, mock flag
pnpm dev
```

## Lint/Format
- Frontend: `cd apps/frontend && pnpm lint`
- Backend: `cd apps/api && ruff check . && ruff format .`
