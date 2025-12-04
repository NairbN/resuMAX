# resuMAX

## Local Development

### Prereqs

- Node 18+ (using v22.21.0)
- Python 3.10+ (using 3.14.0)
- pnpm
- git, VS Code

### Backend (FastAPI)

1. python -m venv .venv
2. source .venv/Scripts/activate # or source .venv/bin/activate
3. pip install fastapi uvicorn[standard] python-dotenv "pydantic[email]" ruff black
4. cd apps/api
5. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   - Health: http://localhost:8000/health

Env file: apps/api/.env (see apps/api/.env.example)

- ENV=local
- DATABASE_URL=postgresql://postgres:postgres@localhost:5432/resumax
- AI_API_KEY=your-local-ai-key
- AUTH_SECRET=dev-jwt-secret
- STORAGE_ENDPOINT=http://localhost:9000
- STORAGE_BUCKET=resumax
- STORAGE_ACCESS_KEY=minioadmin
- STORAGE_SECRET_KEY=minioadmin
- REDIS_URL=redis://localhost:6379/0
- BACKEND_URL=http://localhost:8000
- FRONTEND_URL=http://localhost:3000
- EMAIL_SENDER=noreply@resumax.local

### Frontend (Next.js 14, pnpm)

1. cd apps/frontend
2. pnpm install
3. pnpm dev
   - App: http://localhost:3000
   - Dashboard health check: http://localhost:3000/dashboard

Env file: apps/frontend/.env.local

- NEXT_PUBLIC_API_BASE=http://localhost:8000

### Lint/Format

- Frontend: cd apps/frontend && pnpm lint
- Backend: cd apps/api && ruff check . && ruff format . && black .
