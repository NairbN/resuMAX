# resuMAX - Component Implementation Map

## 1. Purpose
Maps each logical component in resuMAX to the implementation stack, runtime placement, and integration contracts so delivery teams can trace requirements to code and infrastructure.

## 2. Component-to-Implementation Matrix
| Component | Implementation | Key Dependencies | Notes |
| --- | --- | --- | --- |
| Frontend (UI) | Next.js 14 (React + TypeScript, App Router) | `NEXT_PUBLIC_API_BASE_URL`, React Query/fetchers, design system | Uploads via presigned URLs, SSE/websocket or polling for job status, diff/accept/export UI |
| API Gateway & Routing | FastAPI on uvicorn/gunicorn | Pydantic models, JWT middleware, rate limits, SQLAlchemy, OpenAPI client generation | REST + optional SSE/websocket; issues presigned URLs; orchestrates optimize enqueue/status |
| Auth Service | FastAPI module | JWT secrets, email provider, Postgres | Signup/login/refresh/verify/reset; refresh rotation and session revocation |
| Resume Management | FastAPI module + storage adapter | S3/MinIO, Redis/SQS queue, Postgres | Presign upload, persist metadata, enqueue parse task, track parse_status |
| Job Description Management | FastAPI module | Storage adapter, Postgres | Paste/upload JD, sanitize/extract metadata, pair with resumes |
| Optimization Orchestration | FastAPI module | Queue broker (Redis/SQS), AI client, Postgres, Notification service | Validate pairing/credits, enqueue optimize job, status endpoints, audit trail |
| Worker: Parser | Celery/Dramatiq/RQ task | Storage adapter, PDF/DOCX parsers, Postgres | Download from storage, parse to text/sections, emit parse_status and errors |
| Worker: AI Orchestrator | Celery/Dramatiq/RQ task | AI client (OpenAI/Anthropic), prompt-lib, Postgres, Storage | Build prompts, call providers with schema constraints, persist optimized payload, upload artifacts |
| Worker: Exporter | Celery/Dramatiq/RQ task | Playwright/pyppeteer/WeasyPrint, python-docx/docxtpl, Storage | Render PDF/DOCX/text, upload to storage, return signed URLs |
| AI Client & Prompt Library | Python module shared by API/worker | Provider keys, schema validators, mock provider | Provider-agnostic adapter with retries/fallback; mock fixtures for tests |
| Billing/Credits (flagged) | FastAPI routes + worker hooks | Stripe keys/webhook, CreditLedger, feature flag | Gate optimize requests, handle checkout/webhook, adjust credits |
| Notification/Email | Worker task or API hook | Email provider (SES/SendGrid/Mailhog) creds | Verification, password reset, optimization ready/timeouts, receipts |
| Observability | OTel SDK + structlog/loguru | OTEL exporter endpoint, log sink, metrics backend | Traces across API->queue->worker->AI->storage; structured logs/metrics/alerts |

## 3. Data Flow Implementation (Upload -> Optimize -> Export)
- Auth: UI calls FastAPI auth routes to obtain JWT access/refresh; tokens flow on subsequent API calls; refresh rotation enforced.
- Upload & Parse: UI requests `/resumes/presign` -> uploads to S3/MinIO -> calls `/resumes/{id}/parse` -> API enqueues parse task -> worker parses and updates DB status -> UI polls/SSE/websocket for status.
- JD Intake: UI posts `/job-descriptions` (paste/upload) -> API sanitizes/extracts metadata -> stores text/metadata -> ready for pairing.
- Optimize: UI posts `/optimize` -> API validates credits/ownership -> enqueues optimize task with resumeId/jdId/strategy -> worker loads parsed data, calls AI client, validates outputs, stores OptimizationRequest/Version, uploads artifacts -> API exposes `/optimize/{id}` and `/versions` for status/results.
- Export: UI posts `/exports` -> worker renders PDF/DOCX/text -> uploads to storage -> API returns signed URLs; UI downloads.
- Notifications: Optional hooks trigger email/SSE/websocket events on verification, ready/timeout, billing events.

## 4. Integration Contracts (API & Queues)
- REST/SSE/Websocket (FastAPI):
  - Auth: `/auth/register|login|refresh|verify|password-reset/*`
  - Resumes: `/resumes/presign`, `/resumes/{resumeId}/parse`, `/resumes`, `/resumes/{resumeId}`
  - Job Descriptions: `/job-descriptions`, `/job-descriptions/{jdId}`
  - Optimize: `/optimize`, `/optimize/{optimizationId}`, `/optimize/{optimizationId}/accept`
  - Versions: `/versions`, `/versions/{versionId}`
  - Exports: `/exports`
  - Billing (flagged): `/billing/credits`, `/billing/checkout`, `/billing/webhook`
- Queue payloads (Redis/SQS via Celery/Dramatiq/RQ):
  - ParseJob: `{ resumeId, storageKey, mimeType, userId, requestId }`
  - OptimizeJob: `{ optimizationId, resumeId, jobDescriptionId, strategy, userId, requestId }`
  - ExportJob: `{ versionId, format, userId, requestId }`
- Storage conventions: user/record namespacing with signed URLs for uploads/downloads. TODO: confirm exact object key prefixes for resumes/JDs/versions/exports.

## 5. Deployment & Runtime Mapping
- Next.js frontend: container/build output served via CDN/WAF; configured with `NEXT_PUBLIC_API_BASE_URL`.
- FastAPI API: containerized uvicorn/gunicorn behind load balancer; accesses Postgres, Redis/SQS, S3/MinIO; migrations via Alembic on deploy.
- Worker pool: containerized Celery/Dramatiq/RQ workers scaled by queue depth; shares codebase/prompt-lib with API.
- Data plane: PostgreSQL for metadata/state; Redis/SQS for broker; S3/MinIO for file artifacts.
- Observability: OTel exporter sidecar/agent shipping traces/metrics; structured logs to ELK/Datadog; alert rules on API error rate, queue depth, AI failures.
- Email/Notifications: SES/SendGrid/mailhog or webhook-driven notifications, triggered by API/worker events.

## 6. TODOs / Clarifications
- Confirm the chosen queue library (Celery vs Dramatiq vs RQ) and worker start commands for this repo.
- Confirm Alembic migration command path and any seed script entrypoints for local/staging.
- Confirm object storage key prefix conventions and any required virus-scan hooks.
- Confirm OpenAPI client generation flow for sharing contracts between FastAPI and the Next.js frontend.
