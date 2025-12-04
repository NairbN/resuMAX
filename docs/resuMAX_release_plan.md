# resuMAX - Release Plan

## 1. Goals & Scope
- Deliver the MVP that enables verified users to upload resumes/JDs, run AI optimizations with diff controls, and export outputs with reliable queues and observability.
- Align release activities with the revised stack: Next.js frontend, FastAPI API, Celery/Dramatiq/RQ workers on Redis/SQS, Postgres, and S3/MinIO storage.

## 2. Environments & Branching
- Branching: PRs -> `main`; `main` auto-deploys to staging; tagged releases (`v*`) promote to production.
- Environments: Local (docker compose, mock AI), Staging (prod-parity topology with sandbox keys and email verification enforced), Production (managed Postgres/Redis/S3, WAF/CDN, real AI keys).
- Artifacts: container images for frontend, FastAPI API (uvicorn/gunicorn), worker (Celery/Dramatiq/RQ), and any migration/seed jobs published to registry.

## 3. Release Readiness Checklist
- Features: auth/upload/JD/optimize/export flows complete with documented acceptance criteria; SSE/websocket or polling wired for job status.
- Data: Alembic migrations reviewed, idempotent, and tested locally/staging; backup/restore procedure validated before production cut.
- Secrets/config: JWT secrets, DB URL, Redis/SQS broker URLs, S3/MinIO creds/bucket, AI keys, email provider creds, and optional Stripe keys configured per environment.
- Infra: buckets created, Redis/SQS namespaces provisioned, Postgres available with needed extensions, DNS/WAF/CDN ready for frontend/API.
- Workers: concurrency configured for target p90 (<20s) and DLQ/visibility timeout tuned; mock AI enabled for smoke tests.
- Observability: OTel exporter endpoint reachable; dashboards for API error rate, queue depth, AI failures, storage/signature failures; alerts pointing to on-call.
- TODO: confirm final migration command (`uv run alembic upgrade head`?) and worker scale targets for staging/prod.

## 4. Deployment Steps
- Build: `pnpm run build` for Next.js; build/push FastAPI container (uvicorn/gunicorn entrypoint) and worker container (Celery/Dramatiq/RQ entrypoint); version images with tag/commit SHA.
- Staging deploy:
  1. Apply DB migrations (Alembic) once.
  2. Deploy API + worker images; ensure env vars/secrets are mounted.
  3. Deploy frontend; point to staging API origin.
  4. Run smoke tests: auth, upload+parse (mock AI), optimize (mock AI), export, SSE/websocket status updates, signed URL download.
  5. Validate observability signals and queue health.
- Production deploy:
  1. Announce freeze window; ensure backups taken.
  2. Apply DB migrations with rollback plan; pause traffic if needed during irreversible migrations.
  3. Deploy API + worker images; scale worker pool for expected load; set `AI_PROVIDER=openai|anthropic` as appropriate.
  4. Deploy frontend behind CDN/WAF; verify CORS and TLS.
  5. Run smoke tests with limited real AI calls; confirm exports and signed URLs.
  6. Enable feature flags (credits/billing, fallback AI) incrementally after baseline checks.

## 5. Validation & QA Gates
- Automated: lint/unit/integration (frontend + FastAPI + worker) and E2E (mock AI) must pass before tag promotion.
- Manual smoke (staging/prod): auth, upload+parse, optimize, accept changes -> version history -> export; email verification and password reset; SSE/websocket or polling updates; billing gate (if enabled).
- Performance: small-load run to confirm p90 <=20s; verify Celery/SQS retry/backoff paths for timeouts/429s.
- Security: JWT/token rotation verified; presigned URL scopes; tenancy checks; TLS and WAF/CDN rules.

## 6. Rollback & Contingency
- Application: rollback to previous container images; disable new feature flags; drain/stop workers if tasks are failing.
- Database: run Alembic downgrade or restore from backup if safe; ensure migrations are backward-compatible when possible.
- Queue: purge or quarantine failing tasks; increase visibility timeout; switch AI provider to mock to reduce impact during investigation.
- Communication: announce rollback to stakeholders and reset release status board.

## 7. Monitoring & Alerting Post-Release
- Monitors: API 5xx rate, auth failures, queue depth/age, AI timeout/error rate, export failure rate, storage signature errors.
- Logs/Traces: verify requestId propagation API -> queue -> worker -> storage/AI; ensure PII redaction filters enabled.
- Dashboards: p90/p99 latency for optimize, worker throughput, storage latency, email delivery.
- On-call: confirm escalation policy and runbook links for AI provider failures, queue backlog, and storage outages.

## 8. Communication Plan
- Pre-release: share changelog and expected impact; confirm on-call coverage and rollback owner.
- During release: live updates in engineering channel; checkpoint after migrations, after API/worker deploy, after frontend deploy.
- Post-release: summary of validation results, known issues/TODOs, and next enablements (e.g., billing flag).

## 9. TODOs / Open Questions
- Confirm queue provider choice (Redis vs SQS) and DLQ/visibility timeout configuration for production.
- Confirm CDN/domain for frontend and API base URL for each environment.
- Confirm exact seed script (if any) to load demo data after migrations.
- Confirm whether staged rollout or blue/green is required for API/worker pods on Kubernetes/ECS.
