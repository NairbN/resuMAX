# resuMAX - Repository File Structure

## 1. Purpose of This Document
- Provide a clear map of where code, configs, tests, and docs live so engineers can navigate quickly.
- Keep frontend, backend, database, QA, and shared assets organized and aligned to the system architecture.

## 2. Top-Level Repository Layout
- `apps/frontend` — Next.js 14 (App Router) UI.
- `apps/api` — FastAPI application (routes, services, auth, orchestration).
- `apps/worker` — Queue-backed workers for parsing/AI/export/email (shares modules with API).
- `packages/ui` — Design system tokens/components (shared React UI kit).
- `packages/shared` — Cross-cutting clients/types/constants (TS/pygen, OpenAPI client, utilities).
- `packages/prompt-lib` — Prompt templates, AI adapters, schema validators, mock provider fixtures.
- `infra/docker` — Local infra (docker-compose for Postgres, Redis/SQS, MinIO/mail catcher).
- `infra/migrations` — Alembic migrations and seeds.
- `tests/e2e` — Playwright/Cypress E2E suites covering auth > upload > JD > optimize > export.
- `tests/contracts` — API contract/integration tests and fixtures.
- `docs` — Architecture, setup, backlog, test plan, and this file.
- `scripts` — Helper scripts for dev/CI (lint, format, data prep) when added.

## 3. Frontend Folder Structure and Responsibilities
- `apps/frontend/src/app` — App Router routes/layouts, loading/error states, route-level metadata.
- `apps/frontend/src/features` — Domain slices (resume, job-descriptions, optimize, versions, auth, onboarding); each holds page logic, feature hooks, and feature-scoped components.
- `apps/frontend/src/components` — Reusable UI (layout shell, navigation, form primitives) that wrap `packages/ui` tokens/components.
- `apps/frontend/src/hooks` — Cross-feature React hooks (auth/session, polling/SSE, media queries).
- `apps/frontend/src/services/api` — Fetchers/React Query clients, OpenAPI client wrappers, and API helpers.
- `apps/frontend/src/lib` — Client-side utilities (formatting, constants) used across features.
- `apps/frontend/src/styles` — Global styles/theme bridges; tailwind/config files if used.
- `apps/frontend/public` — Static assets.
- `apps/frontend/tests/unit` — Component-level/unit tests (Jest/Vitest).
- `apps/frontend/tests/integration` — Integration tests for feature flows and data hooks.

## 4. Backend Folder Structure and Responsibilities
- `apps/api/app/main.py` — FastAPI entrypoint and app factory.
- `apps/api/app/routes` — Routers, dependencies, request/response schemas tied to FastAPI routes.
- `apps/api/app/core` — Settings/config, security/auth, rate limits, middleware.
- `apps/api/app/models` — SQLAlchemy models and Pydantic DTOs.
- `apps/api/app/services` — Domain services (auth, resumes, JDs, optimize orchestration, exports, billing gate).
- `apps/api/app/clients` — External adapters (AI providers, storage/S3, email, queue broker).
- `apps/api/app/worker` — Shared worker task definitions and queue bindings used by API and `apps/worker`.
- `apps/api/app/db` — Session management, Alembic integration, seed utilities.
- `apps/api/tests/unit` — Service/router unit tests with mocked deps.
- `apps/api/tests/integration` — API contract/integration tests (can be mirrored or coordinated with `tests/contracts`).

## 5. Database / Persistence Assets (migrations, schema, seeds)
- `infra/migrations` — Alembic migration scripts and heads; apply via standard Alembic/CI step.
- `apps/api/app/db` — Database session/config helpers and optional seed utilities.
- `infra/migrations/seeds` (optional) — Seed data for local/staging (demo users, resumes/JDs/versions).
- Storage keys/bucket conventions live in API/worker storage clients; document prefixes in `apps/api/app/clients/storage.py`.

## 6. Testing & QA Structure (where unit/integration/e2e tests live)
- Frontend unit/integration: `apps/frontend/tests/unit`, `apps/frontend/tests/integration`.
- Backend unit/integration: `apps/api/tests/unit`, `apps/api/tests/integration`.
- Worker tests: `apps/worker/tests` (mirrors API service/unit tests for task logic).
- Contract/API tests: `tests/contracts` (can run against local/staging APIs with fixtures/mocks).
- End-to-end/UI: `tests/e2e` (Playwright/Cypress hitting Next.js + API; mock AI provider by default).
- Shared fixtures/mocks: `tests/fixtures` (seed data, mock AI responses, sample resumes/JDs).
- Test assets (sample files) should live under `tests/fixtures/files` to keep binaries out of source folders.

## 7. Shared Utilities / Common Modules
- `packages/shared` — Shared TypeScript/Python clients, OpenAPI-generated types, validation helpers, constants.
- `packages/ui` — Cross-app design system components/tokens; consumed by `apps/frontend`.
- `packages/prompt-lib` — Prompt templates, provider adapters, schema validators, mock AI fixtures used by API and workers.
- `apps/api/app/worker` — Shared queue/task registration that both API and worker runtimes import.
- `apps/frontend/src/lib` — Client-only utilities that should not depend on server-only modules.

## 8. Environment & Config Files (where .env, config files live)
- `apps/api/.env` — FastAPI secrets and service endpoints (JWT, DB, storage, AI, email, queue).
- `apps/frontend/.env.local` — Public frontend envs (API base URL, feature flags, analytics keys).
- `infra/docker/.env` — Docker-compose overrides for local infra services.
- `.env.example` files (per app) — Document required variables for onboarding/CI.
- Config modules: `apps/api/app/core/settings.py` (server config), Next.js config files in `apps/frontend` (e.g., `next.config.js`, `tailwind.config.js`).

## 9. Role-Based Quick Reference (FE, BE, DB, QA)
- Frontend engineers: work in `apps/frontend/src/app`, `apps/frontend/src/features`, `apps/frontend/src/components`, and `apps/frontend/tests/*`; consume shared UI from `packages/ui` and API clients from `packages/shared`.
- Backend engineers: work in `apps/api/app/*` for routers/services/clients/models, plus `apps/api/tests/*`; coordinate worker task definitions in `apps/api/app/worker`.
- Database engineers: manage schemas/migrations in `infra/migrations`, DB config in `apps/api/app/db`, and seeds in `infra/migrations/seeds`.
- QA engineers: place and run suites in `tests/e2e`, `tests/contracts`, `apps/frontend/tests/*`, `apps/api/tests/*`, and `apps/worker/tests`; keep fixtures in `tests/fixtures`.

## 10. How This Structure Aligns With System Architecture
- Next.js frontend (`apps/frontend`) consumes REST/SSE/WebSocket APIs from FastAPI, uploads via signed URLs, and surfaces optimize/versions/export flows.
- FastAPI backend (`apps/api`) hosts auth, resume/JD, optimize orchestration, exports, and billing-gated routes; shares queue/task registration with workers.
- Worker runtime (`apps/worker`) executes parse/AI/export/email tasks using shared prompt library and storage/AI clients.
- Database migrations (`infra/migrations`) manage PostgreSQL schema; storage adapters and queue clients align with S3/MinIO and Redis/SQS choices from the architecture doc.
- Tests/E2E (`tests/*`) validate end-to-end flows, API contracts, and integration points defined in the system architecture and component implementation map.
