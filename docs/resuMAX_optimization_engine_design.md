# resuMAX Optimization Engine Design

## 1. Purpose and Roles
- The optimization engine aligns a user resume to a target job description with truthful, ATS-safe rewrites, a diff-first preview, and an auditable version history.
- Roles in the system:
  - Backend developer: enforce validations, tenancy, orchestration, persistence, and observability.
  - AI prompt engineer: design prompt templates, safety constraints, and provider fallback behavior.
  - QA engineer: verify contracts, edge cases, latency targets, retries/fallbacks, and data integrity.
- Scope: resume and JD pairing, AI-driven optimization, scoring, diff storage, and export readiness; credit gating is feature-flagged.

## 2. End-to-End Orchestration Flow (Request -> AI -> Persistence)
1) Client calls `POST /optimize` with `resumeId` + `jobDescriptionId` (and optional strategy) after client-side validation and auth.
2) API validates ownership, verification status, credit gate (flagged), resume/JD parse status, and size/type constraints; records OptimizationRequest row (status queued) and enqueues OptimizeJob to queue (Redis/SQS).
3) Worker fetches job, loads parsed resume sections and sanitized JD text from Postgres/storage, applies prompt templates, and calls AI via provider-agnostic client (OpenAI primary, Anthropic fallback).
4) Worker validates AI response schema, normalizes sections, computes alignment score, assembles diff and summary, and stores artifacts in Postgres; uploads any large payloads to storage (MinIO/S3) with keyed paths.
5) Worker marks OptimizationRequest to completed (or failed with error_code/message) and may emit notification; version is created on accept call, not during generation.
6) Client polls `GET /optimize/{id}` (or SSE/websocket) for status; when ready, client renders summary/score/diff and later calls `POST /optimize/{id}/accept` to persist accepted changes as OptimizationVersion and trigger exports if requested.

## 3. Backend Service Layer Responsibilities
- Request handlers / API routes (FastAPI)
  - Validate payloads with Pydantic; enforce auth, email verification, rate limits, credit gate (feature-flagged), and tenancy on resume/JD ownership.
  - Routes: `POST /optimize`, `GET /optimize/{id}`, `POST /optimize/{id}/accept`, `GET /versions`, `GET /versions/{id}`.
  - Return structured errors `{code, message, requestId}` and status aligned to UI chips (queued, processing, generating, completed, failed).
- Orchestration service (API layer + worker coordination)
  - Persist OptimizationRequest rows with idempotency key (resumeId + jdId + strategy + userId) to prevent duplicate charges/runs.
  - Enqueue OptimizeJob with trace/requestId; enforce one active optimize per resume/JD pair per user; set visibility timeout aligned to p99 latency.
  - Manage status transitions and emit audit logs; trigger notification/email on ready/timeout when enabled.
- Resume parsing logic (worker)
  - Convert PDF/DOCX to text and sections; store parsed_text and parsed_sections JSON; set parse_status (pending, parsing, completed, failed).
  - Emit errors with actionable codes (unsupported_format, parse_failed, size_exceeded); keep raw file only in storage via signed URL.
- Job description parsing logic (API + worker)
  - Sanitize pasted text; for uploads, extract text from PDF/DOCX/text up to 10 MB; derive metadata (title, company, location).
  - Store sanitized_text and metadata JSON; flag low-quality JD (short length, missing title) for user-visible warnings.
- AI prompt construction module (shared prompt-lib)
  - Templates for summary, gap analysis, per-section rewrite with ATS-safe tone and truthfulness guardrails; slots: candidate headline, skills, experience, education, JD keywords, role/title/company.
  - Enforce instructions: do not invent employers/education/dates; keep format consistent; mark uncertain suggestions.
  - Supports strategy/versioning; include temperature/tokens limits; supports mock provider for local/CI.
- AI response parsing and scoring logic (worker)
  - Expect structured JSON: summary, alignment_score (0-100), per-section suggestions with diff metadata, uncertainty flags.
  - Validate schema; reject hallucinated entities by comparing against parsed resume entities; cap section lengths; normalize whitespace/bullets.
  - Compute diff payloads and aggregate alignment score; derive confidence per section if provider returns tool-call confidence.
- Data persistence handling (API + worker)
  - Tables: OptimizationRequest (job state), OptimizationVersion (accepted result), Resume, JobDescription, ExportArtifact, CreditLedger (flagged).
  - Store prompts/outputs metadata with PII redaction; upload large diffs/output blobs to storage and persist storage_key; include tokens_used for cost tracking.
  - Ensure all writes scoped by userId; soft-delete friendly; emit OTel traces/logs with requestId.

## 4. Optimization API Contract
- Endpoint: `POST /optimize`
  - Input schema: `resumeId` (UUID), `jobDescriptionId` (UUID), `strategy` (optional enum: default, conservative, aggressive_keywords), `clientRequestId` (optional idempotency token).
  - Response: `{ optimizationId, status: queued|processing|generating|completed|failed }`.
- Endpoint: `GET /optimize/{optimizationId}`
  - Response schema (when completed):
    - `optimizationId`, `status`, `resumeId`, `jobDescriptionId`, `strategy`
    - `summary` (bullet strings), `alignmentScore` (0-100), `diff` (per-section original vs optimized with change type), `suggestions` (structured per section), `warnings` (uncertainty, JD quality)
    - `error` only when failed `{ code, message }`
- Endpoint: `POST /optimize/{optimizationId}/accept`
  - Input schema: `acceptedChanges` (per section list or applyAll flag), `notes` optional, `exportFormats` optional array (`pdf|docx|text`) to trigger export jobs.
  - Response: `{ versionId, status: saved, exports?: [{format, downloadUrl? pending until export job completes}] }`.
- Endpoint: `GET /versions` and `GET /versions/{versionId}`
  - Output schema: `versionId`, `optimizationId`, `score`, `acceptedChanges`, `optimizedSections`, `diff`, `createdAt`, `status`, `downloadLinks` (signed URLs if generated).

## 5. Validation Rules
- Auth and verification required; ownership enforced for resumeId/jdId.
- Resume rules: PDF/DOCX only, size <= 5 MB, parse_status must be completed; parsing error codes block optimize.
- JD rules: text/PDF/DOCX <= 10 MB; sanitized_text required; title required; warn on short length (<500 chars) or missing company/location.
- Request rules: one active optimization per resume/JD pair; credit balance >0 when flag on; rate limit optimize endpoint.
- Error messaging: structured codes such as invalid_input, not_verified, insufficient_credits, parse_not_ready, provider_timeout, provider_throttled, schema_validation_failed.

## 6. AI Handling Behavior
- Prompt generation: assemble resume sections + JD keywords; include strict instructions to avoid fabrication, keep ATS-friendly formatting, and surface uncertainty; support strategies (default tone vs aggressive keywords).
- Retry logic: up to 2 retries with exponential backoff on timeouts/429; switch provider (OpenAI -> Anthropic) when configured; circuit breaker when global error rate high.
- Output normalization: schema validation, whitespace/bullet normalization, section ordering preserved, clamp alignment_score 0-100, drop suggestions that introduce new employers/education/dates, mark uncertain suggestions with warnings and default to original text for UI selection.
- Token/tone control: temperature low (conservative), max tokens capped per section; enforce JSON mode/tool-call schema; redact PII in logs; store prompts/outputs for audit with keys only.

## 7. Persistence Expectations
- Metadata stored:
  - OptimizationRequest: status lifecycle, strategy, credits_spent (flagged), error_code/message, requestId, provider metadata.
  - Prompt/response audit: storage keys referencing redacted prompt and AI output blobs; tokens_used and provider model.
  - Alignment score and summary stored for quick list rendering.
- Optimized result storage:
  - OptimizationVersion holds acceptedChanges, optimizedSections, diff; large artifacts stored in object storage with storage_key per user/version.
  - ExportArtifact per format with signed URL TTL tracked; regenerate on expiry via export job.
- Linking to user accounts:
  - All rows keyed by user_id; tenancy checks in queries; signed URLs namespaced per user/resume/jd/version.
  - Soft delete cascades to hide versions/exports while retaining audit as needed; account deletion triggers cleanup jobs.

## 8. Failure Modes and Fallback Behavior
- Validation failures: return 400 with code; preserve client selections; do not enqueue job.
- Queue/worker failure: retry per broker policy; if exhausted, mark job failed with error_code queue_failed and emit notification.
- Provider timeout/429: retry twice, then fallback provider; if still failing, mark failed and keep selections; do not double-charge credits.
- Schema/output invalid: mark failed with schema_validation_failed; optionally re-run with stricter prompt; surface warning to user.
- Long-running jobs: if exceeding SLA, show still-working state; allow optional email notification; auto-fail after max duration with guidance to retry.
- Storage errors: fail gracefully with storage_error; avoid losing job state; allow resume retry once storage healthy.
- Export failures after accept: mark export artifact failed with retry available; keep version intact.

## 9. Future Extensibility Notes
- Additional optimization types: add strategy enums (e.g., executive_tone, concise, skills_focus) and corresponding prompt templates and validators; allow per-section knobs.
- Different scoring engines: plug in ATS scoring service; store separate score type with provider metadata; expose `/optimize/{id}/score`.
- Custom models: support model override per tenant/feature flag; add safety policy configuration; extend provider adapter for self-hosted models.
- Parallelization: enable per-section parallel AI calls with aggregation; maintain ordering and limits.
- Observability growth: add per-section latency metrics, provider success mix, and JD quality scoring signals for triage.
- Governance: expand audit log for prompts/outputs access; add content filters/moderation hooks pre- and post-call.
