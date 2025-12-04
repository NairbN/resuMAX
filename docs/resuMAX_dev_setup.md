# resuMAX - Developer Setup & Onboarding Guide

## 1. Purpose
- Stand up a local resuMAX environment and understand the moving parts (frontend, API, workers, storage, AI).
- Use this as the single source for setup, workflow, and runbook basics.

## 2. System Overview Reference
- Frontend: Next.js 14 (React + TypeScript, App Router) consuming REST from the API; status polling/websocket/SSE for optimize jobs.
- Backend/API: FastAPI on uvicorn exposing REST plus optional events; handles auth, validation via Pydantic, presigned URLs, orchestrates optimize pipeline.
- Workers: Celery/Dramatiq/RQ (Redis or SQS) for parsing, AI calls, exports, email/notifications (not yet wired locally).
- Persistence: PostgreSQL for metadata/state; S3/MinIO for uploads/exports; Redis/SQS for queues.
- AI integration: Provider-agnostic adapter (OpenAI/Anthropic) with prompt library, schema validation, fallback, and mock provider for local/CI.

## 3. Prerequisites & Required Tools
- Git
- Node.js 18+ (using v22.21.0) and pnpm
- Python 3.10+ (using 3.14.0) with venv + pip
- curl for quick API checks
- VS Code (recommended) with ESLint, Tailwind CSS IntelliSense, Python, DotENV
- Optional (future infra): Docker Desktop with compose for Postgres/Redis/MinIO/mail catcher

## 4. Repository Structure Overview
- apps/frontend - Next.js 14 App Router UI (upload, JD intake, optimize, versions, exports).
- apps/api - FastAPI REST API (auth, presign, optimize orchestration, health).
- apps/worker - Queue workers for parse/AI/export/email (placeholder; shares code with API).
- packages/ui - Design system tokens/components (placeholder).
- packages/shared - Shared contracts/clients/constants (placeholder).
- packages/prompt-lib - Prompt templates, AI adapters, schema validators, mock provider fixtures (placeholder).
- infra/docker - Docker-compose for local infra (Postgres, Redis/SQS, MinIO/mail catcher).
- infra/migrations - Alembic migrations and seeds.
- tests/e2e - Playwright/Cypress E2E suites (mock AI default).
- tests/contracts - API contract/integration tests and fixtures.
- docs - Reference docs (architecture, UX, backlog, setup, file structure).
- scripts - Helper scripts for dev/CI when added.

See docs/resuMAX_file_structure.md for detailed layout and per-role guidance.

## 5. Local Environment Setup (current lightweight flow)
1) Clone or open the repo folder.
2) Backend (FastAPI)
   - python -m venv .venv
   - source .venv/Scripts/activate   # Windows Git Bash; use .venv/bin/activate on macOS/Linux
   - pip install fastapi uvicorn[standard] python-dotenv "pydantic[email]" ruff black
   - Create apps/api/.env (see vars below)
   - Run: cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   - Health: http://localhost:8000/health
3) Frontend (Next.js)
   - cd apps/frontend
   - pnpm install
   - Create .env.local with NEXT_PUBLIC_API_BASE=http://localhost:8000
   - Run: pnpm dev
   - UI: http://localhost:3000 (dashboard health check at /dashboard)
4) Worker: placeholder only; wire Celery/Dramatiq/RQ later when queues/storage/DB are configured.
5) Infra (optional, future): docker-compose for Postgres/Redis/MinIO/mail catcher; not required for the current health-check flow.

## 6. Environment Variables (current local usage)
Backend (apps/api/.env)
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

Frontend (apps/frontend/.env.local)
- NEXT_PUBLIC_API_BASE=http://localhost:8000

## 7. Running the Application Locally
Terminal 1 (backend):
- source .venv/Scripts/activate   # or .venv/bin/activate
- cd apps/api
- uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Terminal 2 (frontend):
- cd apps/frontend
- pnpm dev

Checks:
- API health: http://localhost:8000/health
- UI health card: http://localhost:3000/dashboard (shows "API health: ok")

## 8. Lint/Format
- Frontend: cd apps/frontend && pnpm lint
- Backend: cd apps/api && ruff check . && ruff format . && black .

## 9. Optional Next Steps
- Add nav/layout in the Next.js app linking dashboard/upload/job-descriptions/optimize/versions.
- Add a sample POST endpoint in FastAPI and a frontend fetch wrapper to validate JSON round-trip.
- Wire docker-compose for Postgres/Redis/MinIO and swap DATABASE_URL/REDIS_URL/STORAGE_ENDPOINT to point at containers.
- Add worker process using Celery/Dramatiq/RQ once queues/storage are available.

## 10. Troubleshooting
- Backend not reachable: ensure venv is active, uvicorn running on port 8000, and .env present.
- Frontend cannot reach API: confirm NEXT_PUBLIC_API_BASE in .env.local matches backend URL/port; refresh the dev server after env changes.
- CORS/auth later: configure CORS origins and JWT secrets once auth endpoints are added.

## 11. References
- docs/resuMAX_system_architecture.md
- docs/resuMAX_project_index.md
- docs/resuMAX_dev_setup.md (this file)
- docs/resuMAX_file_structure.md
- docs/resuMAX_UI_design_system.md
- docs/resuMAX_UX_UI_design_spec.md
- docs/resuMAX-ux-flows.md
- docs/resuMAX_sprint_backlog.md
