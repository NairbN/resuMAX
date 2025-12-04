# resuMAX - System Architecture

## 1. Overview
- resuMAX is a multi-tenant web application that ingests resumes and job descriptions, runs AI-powered alignment and rewrite pipelines, and returns ATS-friendly, exportable outputs with user-controlled diffs.
- Goals: performant (<20s p90 optimize round-trip), reliable (99.5% monthly uptime), scalable (10k+ users, burstable workers), secure (strict tenancy isolation, encrypted storage, minimal PII handling), and auditable (history, status, and action logs).
- Main components: Next.js frontend, FastAPI (Python) backend API, AI/LLM integration layer with prompt library, PostgreSQL for metadata/state, object storage for files/exports, auth with JWT + email verification, queue-backed workers for parsing/AI/export, observability stack for logs/metrics/traces.

## 2. High-Level Architecture
- Client (browser) talks to the API over HTTPS using short-lived JWT access tokens; refresh tokens kept HttpOnly. API issues pre-signed URLs for uploads/downloads, orchestrates optimization via queue-backed workers, and persists metadata/state in PostgreSQL. Object storage holds raw/optimized documents; AI providers are accessed through a hardened abstraction with retries and guardrails.
- Subsystems:
  - Frontend: Next.js SPA/SSR with design-system components, status polling, websocket/events for job status, and signed URL uploads.
  - Backend API: FastAPI + uvicorn/gunicorn for routing, validation via Pydantic models, auth, rate limiting middleware, and orchestration; exposes REST and optional SSE/websocket for status updates.
  - Authentication & authorization: JWT access + refresh, email verification, password reset, per-resource ownership checks, optional role support for admin.
  - AI / LLM layer: Prompt builder + provider clients (OpenAI/Anthropic) running inside workers; schema-guided outputs and validation.
  - File storage: S3/MinIO for resumes, JDs, parsed text exports, and generated PDFs/DOCX with short-lived signed URLs.
  - Database: PostgreSQL for users, resumes, JDs, optimization jobs, versions, credits/billing, and audit logs.
  - Messaging/queue: Redis-backed Celery/Dramatiq/RQ or SQS for async parsing/optimization/export with retries and DLQ.

```
Users (Browser - Next.js)
        |
   HTTPS + JWT
        v
[API Gateway / Backend (FastAPI)]
   |-- Auth & Rate Limit
   |-- Resume/JD APIs ----> [PostgreSQL] (metadata/state)
   |-- Signed URLs --------> [Object Storage (S3/MinIO)]
   |-- Enqueue Optimize ---> [Queue (Redis/SQS)]
   |                         |
   |                         v
   |                  [Worker Pods]
   |                     |-- Parser (PDF/DOCX -> text/sections)
   |                     |-- Prompt Builder -> [AI Providers]
   |                     |-- Exporter (PDF/DOCX/Text) -> Storage
   |-- Webhooks/Email -> [Email/Notification Service]
   v
[Observability: logs/metrics/traces]
```

## 3. Technology Stack (Proposed)
- Frontend: Next.js 14 (React + TypeScript) with App Router; SSR/SSG for auth and marketing pages, client-side flows for uploads/diffs; integrates well with design system and rich status handling.
- Backend: FastAPI (Python) on uvicorn/gunicorn; Pydantic models for request/response validation; dependency injection for auth/rate limits; modular routers/services; Celery/Dramatiq/RQ workers for background jobs.
- Database: PostgreSQL (with JSONB for parsed sections, AI artifacts) for relational integrity (users<->resumes<->JDs<->versions) and transactional updates.
- File storage: AWS S3 in production; MinIO in local/staging. Pre-signed URLs avoid backend load and preserve privacy.
- Auth: JWT (access/refresh) with email/password; email verification and password reset via signed tokens + email service (e.g., SES/SendGrid). Optional OAuth provider can be added later.
- AI providers: OpenAI GPT-4.1/GPT-4.1-mini primary; Anthropic Claude as fallback. Provider-agnostic adapter enables routing, retries, and testing with mock providers.
- Queue: Redis (Celery/Dramatiq/RQ) or AWS SQS for async optimize/export, with visibility timeouts, DLQ, and exponential backoff.
- Export/rendering: headless Chromium via Playwright/pyppeteer or WeasyPrint for PDF; python-docx/docxtpl for DOCX; text export direct from optimized content.
- Observability: OpenTelemetry traces + structured JSON logs (e.g., structlog/loguru) to ELK/Datadog; metrics via Prometheus-compatible exporter.

## 4. Logical Components & Responsibilities
- API Gateway / Routing
  - Responsibilities: request validation, auth guards, rate limits, tenancy enforcement, routing to domain services.
  - Inputs: HTTP requests with JWT; Outputs: JSON responses, SSE/websocket events.
- Auth Service
  - Responsibilities: sign up/login, email verification tokens, password reset, refresh token rotation, session revocation.
  - Inputs: credentials; Outputs: access/refresh tokens, verification emails, error codes.
- User Profile Service
  - Responsibilities: profile updates (name, email), default job preferences, notification settings.
  - Interactions: PostgreSQL (users), Email service (verification changes).
- Resume Management Service
  - Responsibilities: create resume records, pre-sign upload URLs, trigger parsing jobs, track parse status, rename/delete, list versions.
  - Inputs: file metadata; Outputs: pre-signed URLs, resume IDs, status.
  - Interactions: Storage adapter, Queue (parse job), DB.
- Job Description Management Service
  - Responsibilities: intake paste/file, sanitize, extract metadata (title/company/location), store text, pair with resumes, rename/delete.
  - Interactions: Storage adapter, Parser (if file), DB.
- Parsing Service (worker)
  - Responsibilities: convert PDF/DOCX to text, detect sections/entities, populate structured sections with confidence; emits parse_status.
  - Inputs: storage key, mime type; Outputs: parsed_text, parsed_sections JSON, errors.
- Optimization Orchestration Service
  - Responsibilities: validate resume+JD, check credits (if enabled), enqueue optimization job, manage job state, persist results, compute alignment score, audit accepted changes.
  - Interactions: Queue, AI Client, DB, Storage, Notification (ready emails), Billing.
- AI Client / Prompt Library
  - Responsibilities: build prompts (summary, gap analysis, rewrite per section), call providers with schema constraints, enforce safety/length, retries, and fallbacks.
  - Inputs: parsed resume, sanitized JD, user preferences; Outputs: structured optimization payload (summary, suggested changes, rewritten sections, score).
- Versioning & History Service
  - Responsibilities: persist optimized versions, diffs, acceptance choices, download references; support re-run with prior resume/JD.
  - Interactions: DB, Storage, Exporter.
- Export Service
  - Responsibilities: render PDF/DOCX/text, upload to storage, return download URLs, label version artifacts.
- Billing/Credits Service (feature-flagged)
  - Responsibilities: integrate with Stripe for purchases, maintain credit ledger, enforce credit gates on optimization, refunds/adjustments.
- Notification/Email Service
  - Responsibilities: email verification, password reset, optimization ready/timeouts, billing receipts.
- File Storage Adapter
  - Responsibilities: generate pre-signed upload/download URLs, enforce path conventions, set TTLs, server-side encryption flags, virus scan hook (optional).
- Observability/Analytics
  - Responsibilities: structured logging, metrics (latency, queue depth, AI failures), tracing, funnel events for onboarding and optimization completion.

## 5. API Design (High-Level)
**Auth**
- `POST /auth/register` - create account; body `{ email, password, name }`; response `{ user, accessToken, refreshToken }`.
- `POST /auth/login` - authenticate; body `{ email, password }`; response tokens as above.
- `POST /auth/refresh` - rotate refresh; body `{ refreshToken }`; response `{ accessToken, refreshToken }`.
- `POST /auth/verify` - confirm email; body `{ token }`; response `{ status }`.
- `POST /auth/password-reset/request` - body `{ email }`; response `{ status }`.
- `POST /auth/password-reset/confirm` - body `{ token, newPassword }`; response `{ status }`.

**Users**
- `GET /users/me` - fetch profile; response `{ id, email, name, preferences }`.
- `PUT /users/me` - update profile/preferences; body `{ name?, preferences? }`; response updated user.

**Resumes**
- `POST /resumes/presign` - request upload URL; body `{ filename, mimeType, size }`; response `{ uploadUrl, resumeId }`.
- `POST /resumes/{resumeId}/parse` - trigger parse after upload; response `{ status }`.
- `GET /resumes` - list resumes with statuses, scores, timestamps.
- `GET /resumes/{resumeId}` - get resume metadata, parsed sections, status.
- `PATCH /resumes/{resumeId}` - rename or update labels; body `{ title? }`.
- `DELETE /resumes/{resumeId}` - soft-delete + storage cleanup.

**Job Descriptions**
- `POST /job-descriptions` - create JD; body `{ title, company?, location?, text? }` or file reference; response `{ jobDescriptionId }`.
- `GET /job-descriptions` - list JDs.
- `GET /job-descriptions/{jdId}` - fetch JD details and sanitized text.
- `PATCH /job-descriptions/{jdId}` - rename/update metadata.
- `DELETE /job-descriptions/{jdId}` - delete JD and storage artifact.

**Optimization**
- `POST /optimize` - enqueue optimization; body `{ resumeId, jobDescriptionId, strategy? }`; response `{ optimizationId, status }`.
- `GET /optimize/{optimizationId}` - status + summary/diff payload when ready.
- `POST /optimize/{optimizationId}/accept` - persist accepted changes; body `{ acceptedChanges, applyAll? }`; response `{ versionId }`.
- `GET /versions` - list optimized versions/history with timestamps, score, status.
- `GET /versions/{versionId}` - fetch version metadata and download links.

**Exports**
- `POST /exports` - generate download artifact; body `{ versionId, format: "pdf"|"docx"|"text" }`; response `{ downloadUrl }`.

**Billing (optional)**
- `GET /billing/credits` - current balance and plan.
- `POST /billing/checkout` - initiate purchase; response checkout session URL.
- `POST /billing/webhook` - Stripe webhook handler (secured via secret header).

## 6. Data Model / Schema
**User**
| Field | Type | Description |
| --- | --- | --- |
| id | uuid | PK |
| email | text (unique) | Login identifier |
| password_hash | text | Argon2 hash |
| email_verified_at | timestamp | Null until verified |
| name | text | Display name |
| preferences | jsonb | Default job preferences, notification toggles |
| role | text | `user` or `admin` |
| created_at/updated_at | timestamps | Auditing |

**Resume**
| Field | Type | Description |
| --- | --- | --- |
| id | uuid | PK |
| user_id | uuid | FK -> users |
| title | text | User-friendly name |
| original_filename | text | Uploaded name |
| storage_key | text | S3/MinIO path |
| mime_type | text | pdf/docx |
| size_mb | numeric | Validation/logs |
| parse_status | enum | pending/parsing/completed/failed |
| parsed_text | text | Extracted text |
| parsed_sections | jsonb | Structured sections/entities |
| last_score | numeric | Latest alignment score (nullable) |
| deleted_at | timestamp | Soft delete |
| created_at/updated_at | timestamps | Auditing |

**JobDescription**
| Field | Type | Description |
| --- | --- | --- |
| id | uuid | PK |
| user_id | uuid | FK -> users |
| title | text | Required label |
| company | text | Optional |
| location | text | Optional |
| source_type | enum | paste/upload |
| storage_key | text | If file uploaded |
| sanitized_text | text | Cleaned JD text |
| metadata | jsonb | Extracted fields (salary, seniority) |
| created_at/updated_at | timestamps | Auditing |

**OptimizationRequest**
| Field | Type | Description |
| --- | --- | --- |
| id | uuid | PK |
| user_id | uuid | FK -> users |
| resume_id | uuid | FK -> resumes |
| job_description_id | uuid | FK -> job_descriptions |
| status | enum | queued/processing/generating/completed/failed |
| strategy | text | prompt variant/version |
| credits_spent | int | If billing enabled |
| summary | text | High-level changes |
| alignment_score | numeric | 0-100 |
| error_code/message | text | If failed |
| created_at/updated_at/completed_at | timestamps | Auditing |

**OptimizationVersion (Result)**
| Field | Type | Description |
| --- | --- | --- |
| id | uuid | PK |
| optimization_id | uuid | FK -> optimization_requests |
| user_id | uuid | FK -> users |
| accepted_changes | jsonb | Per-section acceptance state |
| optimized_sections | jsonb | Final accepted text |
| diff | jsonb | Original vs optimized diff |
| output_storage_key | text | Final rendered artifact (canonical) |
| tokens_used | int | For cost tracking |
| created_at | timestamp | Auditing |

**ExportArtifact**
| Field | Type | Description |
| --- | --- | --- |
| id | uuid | PK |
| version_id | uuid | FK -> optimization_versions |
| format | enum | pdf/docx/text |
| storage_key | text | File path |
| expires_at | timestamp | For download validity |
| created_at | timestamp | Auditing |

**CreditLedger (optional)**
| Field | Type | Description |
| --- | --- | --- |
| id | uuid | PK |
| user_id | uuid | FK -> users |
| delta | int | Positive purchase / negative spend |
| reason | text | optimization, refund, manual |
| stripe_event_id | text | Trace to Stripe |
| balance_after | int | Snapshot |
| created_at | timestamp | Auditing |

Relationships: User has many Resumes, JobDescriptions, OptimizationRequests, OptimizationVersions, CreditLedger entries. OptimizationRequest links one Resume + one JD. OptimizationVersion belongs to an OptimizationRequest and User. ExportArtifacts belong to a Version.

## 7. AI Integration Architecture
- Flow: API validates request and enqueues job with resumeId + jdId + strategy. Worker loads parsed resume + sanitized JD, builds prompts (summary, gap analysis, rewrite per section), calls AI provider via AI Client with schema constraints (JSON mode / tool calls) and max tokens.
- Prompt construction: centralized templates with slotting for resume sections, JD keywords, tone rules (conservative/ATS-friendly), and truthfulness instructions ("do not invent employers/education"). Per-section rewrite prompts to keep structure.
- Validation: post-call schema validation; business rules to reject hallucinated entities (e.g., new employer/date) by comparing against parsed resume entities; enforce size limits; scrub PII from logs.
- Error handling: retries with exponential backoff (max 2) on timeouts/429; provider fallback (OpenAI -> Anthropic) when enabled; mark job failed with error_code and emit toast/email.
- Safety: optional moderation check on inputs; clamp outputs to deterministic format; store prompts/outputs in audit log table with redaction of PII.
- Extensibility: AI Client interface supports multiple providers, offline mock for tests, and feature-flagged prompt versions.

## 8. Security & Privacy Considerations
- Authentication: JWT access (short TTL) + refresh rotation; email verification required before uploads; password hashed with Argon2id; option to add 2FA later.
- Authorization: per-resource ownership checks on every request; optional admin role with scoped endpoints; DB-level row filters for user_id.
- Data protection: TLS for all traffic; storage server-side encryption (SSE-S3/KMS); DB encryption at rest; secrets in managed store (SSM/Secrets Manager).
- File handling: pre-signed URLs scoped to user, short TTL; object keys namespaced by user/record IDs; optional virus scan on upload; prevent public ACLs.
- PII minimization: avoid logging raw resume/JD; redact tokens/PII in logs; restrict support access; audit log reads/writes of sensitive records.
- Rate limiting & abuse: IP/user rate limits on auth and optimize; captcha on auth/password-reset after threshold; credit gating to deter abuse.
- Data lifecycle: soft-delete with eventual hard-delete job; user-triggered account deletion removes storage artifacts and related records; retention policies configurable.
- Compliance readiness: track consent to terms/privacy; maintain audit logs for access; configurable data residency via storage bucket region.

## 9. Error Handling & Observability
- API errors: structured JSON `{ code, message, details?, requestId }`; client shows inline errors with retry hints; fallbacks for long-running optimize (polling + optional email notification).
- Logging: structured logs (requestId, userId, route, latency, status, error_code, provider) at API and worker; PII redaction filters.
- Metrics: request latency, error rate, auth failures, parse success rate, optimization p90/p99 latency, AI timeout/error counts, queue depth, worker CPU/memory, export success/fail.
- Tracing: OpenTelemetry spans across API -> queue -> worker -> AI call -> storage; propagate requestId in headers and logs.
- Alerting: thresholds on 5xx rate, AI failure rate, queue backlog, storage/signature failures, and auth anomalies trigger pager/notifications.

## 10. Performance & Scalability
- Expected usage: MVP target 500 DAU, ~2-3 optimize jobs/user/day; ~20 MB daily ingest per user.
- Scaling approach: stateless API pods behind load balancer; horizontal autoscale on CPU/RPS; separate worker pool scaling on queue depth; storage/database managed services with read replicas for heavy reads.
- Bottlenecks: AI calls dominate latency - mitigate with streaming where possible, parallel section generation, caching JD keyword extraction, and job queue to smooth bursts.
- Caching: in-memory/Redis cache for auth keys, feature flags, JD metadata; signed URL generation cached per artifact where safe.
- Concurrency controls: limit concurrent optimize per user, circuit breaker on provider errors, bounded retry counts, idempotency keys for optimize and exports.

## 11. Environments & Deployment
- Local: Docker Compose (PostgreSQL, Redis/MinIO) + seeded demo data; `npm run dev` for Next.js and `uvicorn app.main:app --reload` (or equivalent) for FastAPI; env vars via `.env.local`; mock AI provider for offline work.
- Staging: Same topology as prod (reduced scale); gated behind auth; connects to sandbox AI/provider keys; run migrations automatically; feature flags to test billing/credits.
- Production: Containerized services deployed via CI/CD (GitHub Actions) to Kubernetes/ECS; rolling deploy with health checks; DB migrations gated; WAF + CDN (for static assets) + TLS termination at load balancer.
- CI/CD: lint/tests -> build -> unit/integration (API + worker) -> deploy; migration step with rollback plan; secrets from cloud secret manager.
- Infrastructure as Code: Terraform for S3/MinIO buckets, DB, Redis/SQS, email/SES, secrets, and observability stack.

## 12. Future Extensions
- ATS scoring: add Scoring Service using rules + AI scoring prompt; store per-version ATS report; expose `/optimize/{id}/score`.
- Cover letter generation: reuse AI Client with new prompt; model `CoverLetter` tied to resume/JD; export via existing exporter.
- LinkedIn integration: OAuth flow to ingest profile; new `LinkedProfile` model; mapping service to seed resumes and suggest gaps.
- Subscription/billing: Stripe subscriptions with webhooks updating `CreditLedger` and `Plan` fields; add metering for AI/token usage.
- Collaboration/sharing: future role-based sharing per resume/version with scoped signed URLs and activity audit trail.
