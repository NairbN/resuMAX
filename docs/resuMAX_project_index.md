# resuMAX Project Index

## 1. Product Overview
- resuMAX tailors user resumes to target job descriptions via AI rewrites, diff-first preview, and ATS-safe exports.
- Targets fast activation (<10 minutes) with guided steps, privacy reassurance, and auditable history.
- Designed for job seekers with optional admin/support operations and feature-flagged credits/billing.

## 2. MVP Scope
- In: auth (email/password, verification, reset), resume upload/parse (PDF/DOCX <=5 MB), JD intake (paste/upload <=10 MB), pairing, AI optimization with summary/diff, accept-all/per-change, version history, exports (PDF/DOCX/text), dashboard statuses, basic profile.
- Optional flag: credit gating/payments via Stripe; ready but toggled by env flag.
- Out: cover letters, ATS submission, LinkedIn import, collaboration/sharing, multi-language, mobile apps, advanced analytics.

## 3. Core User Flows
- Onboarding checklist: Upload resume -> Add job description -> Optimize & download; persists and re-openable.
- Resume upload/parse with validation, progress, retry/re-run parse, privacy note.
- JD intake with paste/upload, sanitization, metadata extraction (title/company/location), save and pair.
- Optimization workspace: select resume+JD, status chips (queued > processing > generating > ready, "<20s typical"), summary + alignment score, side-by-side/unified diff, accept-all/per-change, uncertainty warnings default to original.
- Save/version + exports: preview, download PDF/DOCX, copy text, history with statuses/scores, rename/delete, signed URLs.
- Auth flows: signup/login, email verification gate, password reset, profile updates.

## 4. Tech Stack Summary
- Frontend: Next.js 14 (React, TypeScript, App Router), design system components, React Query/polling or SSE/websocket for status, presigned URL uploads.
- Backend: FastAPI (Python) with Pydantic validation, JWT auth/refresh, rate limits, REST + optional SSE/websocket, structured JSON errors.
- Workers: Celery/Dramatiq/RQ on Redis or SQS for parsing, AI orchestration, retries/backoff, export rendering, notifications.
- Data: PostgreSQL metadata/state; S3/MinIO for resumes/JDs/versions/exports via signed URLs; Redis/SQS as queue broker.
- AI layer: provider-agnostic client (OpenAI GPT-4.1 primary, Anthropic fallback), prompt library with schema validation, mock provider for local/CI.
- Rendering/exports: headless Chromium/Playwright/pyppeteer or WeasyPrint for PDF; python-docx/docxtpl for DOCX.
- Observability: OpenTelemetry traces, structured logs (requestId), metrics/alerts on latency, queue depth, AI failures, storage/signature errors.

## 5. Architectural Responsibilities
- Frontend: enforce client-side validation and UX flows, upload via signed URLs, surface statuses, diffs, and exports, honor verification/credit gates.
- API gateway/services: auth, presign URLs, pairing validation, credit checks (flagged), job orchestration, status endpoints, audit logging, rate limits.
- Parsing service: convert PDF/DOCX to text/sections/entities with confidence; emit parse_status updates.
- Optimization service: build prompts, call AI with retries/fallback, enforce truthfulness and section schema, compute alignment score, store diffs and accepted changes.
- Versioning/history: persist versions, diffs, scores, audit of acceptances; serve lists/details.
- Export service: render PDF/DOCX/text artifacts, upload to storage, generate signed download URLs.
- Notification/email: verification, password reset, optimization ready/timeout, billing receipts.
- Billing/credits (flagged): manage ledger, deductions, checkout/webhooks; gate optimize when balance empty.

## 6. Repo / Folder Structure Assumptions
- apps/frontend: Next.js UI, onboarding checklist, upload/JD/optimize/history/exports flows.
- apps/api: FastAPI routes (auth, resumes, JDs, optimize, versions, exports, billing, observability).
- apps/worker: Celery/Dramatiq/RQ tasks for parse/optimize/export/email/cleanup.
- packages/ui: design system tokens/components (buttons, upload tiles, cards, steppers, modals, toasts).
- packages/shared: shared contracts/clients/constants (e.g., OpenAPI TS client); Python shared module TBD.
- packages/prompt-lib: prompt templates, AI adapters, schema validators, mock provider fixtures.
- infra/docker: docker-compose for Postgres/Redis/MinIO/mail catcher; bucket/init scripts.
- infra/migrations: Alembic/SQLAlchemy migrations and seeds.
- tests/e2e: Playwright/Cypress E2E (auth > upload > JD > optimize > export) using mock AI.
- tests/contracts: API contract/integration tests and fixtures.
- docs: reference docs listed in index.

## 7. Integration Points
- Storage: S3/MinIO via presigned upload/download URLs; object keys namespaced per user/record; short TTL; optional virus scan hook.
- AI providers: OpenAI/Anthropic via adapter with retries/backoff/fallback; mock provider for local/CI; tone conservative and grounded.
- Queue: Redis or SQS for async parse/optimize/export; DLQ/visibility timeout configured; worker autoscale on depth.
- Email service: SES/SendGrid/mailhog for verification, reset, ready/timeouts; env-driven sender.
- Payments (feature-flagged): Stripe checkout/webhooks managing credit ledger and gating optimize.
- Observability: OTel exporter endpoint, dashboards/alerts for API/worker/queue/AI/storage health.
- Rendering: headless Chromium/WeasyPrint for PDF; python-docx/docxtpl for DOCX.

## 8. Non-Functional Expectations
- Performance: optimization p90 <=20s (p99 <=30s); uploads/exports responsive; retries capped (max 2) with backoff.
- Availability/reliability: 99.5% monthly uptime target; queue-backed workflows with DLQ; idempotent optimize/export jobs; signed URL TTL and clock skew considered.
- Security/privacy: TLS everywhere, JWT short-lived access + refresh rotation, email verification required before uploads, strict tenancy checks, encrypted storage, PII redaction in logs, audit trails for sensitive actions.
- Scalability: 10k+ users storing ~20 optimized resumes each; horizontal scale API/workers; storage and DB managed services.
- Compliance/readiness: data deletion on request, soft-delete with cleanup, audit logging, consent tracking.
- Observability: structured logs with requestId, metrics on latency/error/queue depth/AI failures/export failures, traces across API->queue->worker->providers.

## 9. Authoritative Document Index (table referencing docs)
| Document | Purpose |
| --- | --- |
| docs/resuMAX_BRD.md | Business goals, actors, MVP scope, acceptance criteria, risks. |
| docs/resuMAX_UX_UI_design_spec.md | UX intent, personas, flows, wireframes, style, and copy guidelines. |
| docs/resuMAX-ux-flows.md | Detailed clickthrough flows, screen responsibilities, edge cases. |
| docs/resuMAX_UI_design_system.md | Visual tokens, components, spacing, typography, interaction states. |
| docs/resuMAX_system_architecture.md | System components, stack, data model, API outline, AI/privacy/observability. |
| docs/resuMAX_sprint_backlog.md | MVP epics, stories, acceptance criteria, tasks, dependencies, out-of-scope. |
| docs/resuMAX_component_implementation_map.md | Mapping of logical components to stack/runtime, queue payloads, TODOs. |
| docs/resuMAX_test_plan.md | QA scope, journeys, test cases, non-functional and negative coverage. |
| docs/resuMAX_dev_setup.md | Local setup, tooling, env vars, repo conventions, workflows. |
| docs/resuMAX_release_plan.md | Environments, readiness checklist, deploy/rollback, monitoring/comm plan. |

## 10. Guidance for AI Assistants (how to use docs properly)
- Use this index to locate detail; cite the specific doc/section you rely on instead of rephrasing whole passages.
- Prefer stable rules (limits, states, feature flags) from BRD/backlog/architecture; avoid inventing behaviors not recorded.
- When generating UX/UI content, align to design spec and design system tokens; keep conservative tone and privacy cues.
- When generating code/tasks, mirror repo structure and API contracts from architecture/implementation map; keep feature flags and env vars explicit.
- Respect privacy: do not fabricate user data or add claims absent from resume/JD; note uncertainty warnings where applicable.
- For tests, tie scenarios to acceptance criteria and test plan; default to mock AI unless real keys/flags are confirmed.

## 11. Guardrails / Do & Do Not rules
- Do: enforce file limits (resume PDF/DOCX <=5 MB; JD text/PDF/DOCX <=10 MB), email verification before uploads, pairing validation before optimize, credit gate when enabled, conservative/ATS-friendly tone, signed URLs for storage, retries capped with clear status messaging.
- Do: preserve user inputs across errors, provide diff-first review with accept-all/per-change, store audit of accepted changes, use structured errors {code,message,requestId}.
- Do Not: invent employers/education/dates/skills not in resume, bypass tenancy or signed URL scoping, double-charge credits, log PII or raw documents, ship features marked out-of-scope (cover letters, LinkedIn import, ATS submissions, collaboration, multi-language).
- Do Not: allow optimization/download without valid resume+JD pairing or when verification/credit gates block the action; avoid silent retries beyond configured limits.

## 12. Version Notes
- Source docs version: 0.1 dated 2025-12-03; this index summarizes stable MVP truths only.
- Stack choices are Next.js + FastAPI + worker queue (Redis/SQS) with PostgreSQL and S3/MinIO; AI provider primary OpenAI GPT-4.1 with Anthropic fallback.
- Feature flags: credits/billing optional; mock AI enabled for local/CI; SSE/websocket vs polling for status is implementation-dependent but must deliver live job states.
