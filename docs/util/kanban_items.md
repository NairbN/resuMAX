# resuMAX Kanban Items

Copy each ticket into your board; story details/AC are included for quick context.

## AUTH-1 — Sign up, verify email, log in
- User story: As a job seeker, I want to sign up, verify my email, and log in so that I can securely access the dashboard.
- Acceptance criteria:
  - Unverified signup blocks uploads with banner + resend verification.
  - Valid login issues access/refresh tokens and lands on dashboard.
  - Invalid login shows inline error, rate limits excessive attempts.
  - Verified account refreshes tokens without re-login until expiry.
- Tickets:
  - AUTH-1 FE (High, 3 pts): Signup/login forms with inline validation; verification banner gating uploads.
  - AUTH-1 BE (High, 5 pts): Register/login/refresh/verify endpoints with Pydantic validation, rate limits, JWT issuance.
  - AUTH-1 DB (High, 3 pts): User + verification token schema/migration; email indices.
  - AUTH-1 QA (High, 3 pts): Auth happy/invalid paths, unverified upload block, token refresh tests.

## AUTH-2 — Reset password, manage profile
- User story: As a user, I want to reset my password and manage my profile so that I can regain access and keep my account current.
- Acceptance criteria:
  - Reset request sends rate-limited email with time-bound token.
  - Valid reset token sets new strong password; prior sessions revoked.
  - Profile updates persist and reflect on reload.
- Tickets:
  - AUTH-2 FE (Medium, 3 pts): Password reset request/confirm screens with password rules; profile edit form.
  - AUTH-2 BE (High, 3 pts): Reset request/confirm endpoints, token expiry, session revocation.
  - AUTH-2 DB (Medium, 2 pts): Password reset token table/fields; audit profile updates.
  - AUTH-2 QA (Medium, 2 pts): Reset flow tests, strength rules, profile persistence regression.

## RES-1 — Resume upload and parse
- User story: As a job seeker, I want to upload my resume (PDF/DOCX <=5 MB) and see parse status so that I know it is ready for optimization.
- Acceptance criteria:
  - Valid PDF/DOCX <=5 MB passes client checks; progress + cancel visible.
  - On success + parse complete, detected sections summary and completed chip.
  - On parse failure, inline banner with retry guidance; file available to retry.
  - Unsupported file/size keeps CTA disabled with inline rule.
- Tickets:
  - RES-1 FE (High, 3 pts): Upload dropzone with type/size checks, progress, cancel, parse status display.
  - RES-1 BE (High, 3 pts): POST /resumes/presign and /resumes/{id}/parse with validation, presigned URLs, parse job enqueue.
  - RES-1 DB (High, 3 pts): Resume table migration; indexes for status.
  - RES-1 QA (High, 2 pts): Upload/parse success, invalid file/size, parse failure retry; verify worker status updates.

## RES-2 — Resume management
- User story: As a job seeker, I want to view, rename, or delete my uploaded resumes with clear statuses so that I can manage my library.
- Acceptance criteria:
  - Dashboard shows cards with status (pending/parsing/completed/failed), timestamps, rename/delete actions.
  - Rename persists and reflects in selectors.
  - Delete is soft-delete, hidden from lists, triggers storage cleanup.
- Tickets:
  - RES-2 FE (Medium, 2 pts): Dashboard cards/list with status chips, rename/delete overflow menu, timestamps.
  - RES-2 BE (Medium, 3 pts): PATCH/DELETE resume endpoints with ownership checks, soft-delete, storage cleanup enqueue.
  - RES-2 DB (Medium, 2 pts): Deleted_at handling; trigger/task kickoff for storage cleanup.
  - RES-2 QA (Medium, 2 pts): Rename/delete flows, status rendering, soft-delete isolation tests.

## JD-1 — Job description intake
- User story: As a job seeker, I want to paste or upload a job description (<=10 MB) with title/company/location so that it is labeled for pairing.
- Acceptance criteria:
  - Paste/upload JD text/PDF/DOCX <=10 MB; sanitize text; extract/edit title/company/location.
  - Missing metadata prompts for title before saving.
  - On upload failure, pasted text persists for retry.
- Tickets:
  - JD-1 FE (High, 2 pts): JD paste/upload UI with sanitization note, metadata inputs, sticky save CTA.
  - JD-1 BE (High, 3 pts): POST /job-descriptions with sanitize/extract; enforce size/type limits; storage handling.
  - JD-1 AI (Low, 1 pt): Metadata extraction prompt fallback for missing title/company.
  - JD-1 DB (High, 2 pts): JD table migration with sanitized_text and metadata JSONB.
  - JD-1 QA (Medium, 2 pts): Missing title block, paste preservation on failure, metadata extraction smoke tests.

## JD-2 — Pair resume and JD
- User story: As a job seeker, I want to pair a JD to a resume and see validation so that I can start optimization confidently.
- Acceptance criteria:
  - With resume + JD selected, validation confirms readiness before enabling Optimize.
  - Invalid/missing selections keep Optimize disabled with guidance.
  - Saved pairing is remembered on return.
- Tickets:
  - JD-2 FE (High, 2 pts): Pairing selector UI with validation copy; disable Optimize until valid.
  - JD-2 BE (Medium, 2 pts): Pairing validation in optimize request; persist last selected resume/JD.
  - JD-2 DB (Low, 1 pt): Store last_selected_resume_id/jd_id in user preferences.
  - JD-2 QA (Medium, 2 pts): Pairing validation, remembered selection, invalid selection errors.

## OPT-1 — Optimization UX and save
- User story: As a job seeker, I want to run optimization with summary, diff, and apply-all/per-change controls so that I can tailor my resume safely.
- Acceptance criteria:
  - Status chips show queued > processing > generating with "<20s typical".
  - Preview shows summary, alignment score, diff; accept-all/per-change toggles.
  - Saving accepted/rejected changes creates version with audit.
  - Uncertainty flags default to original text with warning.
- Tickets:
  - OPT-1 FE (High, 5 pts): Optimization workspace with status chips, summary panel, diff modes, accept-all/per-change, sticky footer.
  - OPT-1 BE (High, 5 pts): POST /optimize enqueue; GET status with summary/diff; POST accept changes to create version; enqueue optimize job.
  - OPT-1 AI (High, 5 pts): Prompt templates (summary/gap/rewrite), schema validation, conservative tone, uncertainty flagging in worker.
  - OPT-1 DB (High, 3 pts): OptimizationRequest and OptimizationVersion migrations; store diffs/accepted_changes JSONB.
  - OPT-1 QA (High, 3 pts): End-to-end optimize flow, diff correctness, accept-all/per-change persistence, uncertainty warnings.

## OPT-2 — Reliability, retries, credit gate
- User story: As a user, I want reliable optimization with retries, timeout handling, and credit gating (when enabled) so that I am not blocked by failures.
- Acceptance criteria:
  - Timeout/429 retries up to 2 times; failures surface user-facing error.
  - Provider fallback routes to secondary before failing.
  - Zero credits (flag on) gates optimize with modal to Billing.
  - Retry preserves previous selections and resets status appropriately.
- Tickets:
  - OPT-2 FE (High, 3 pts): Error/timeout handling UI, retry, credit gate modal (feature-flag).
  - OPT-2 BE (High, 4 pts): Retry/backoff logic, provider fallback, credit check before enqueue, error codes surfaced.
  - OPT-2 AI (High, 3 pts): Provider adapter with fallback routing, deterministic validation, capped tokens.
  - OPT-2 DB (Medium, 2 pts): Credit ledger (flagged), error_code/message fields on optimization jobs.
  - OPT-2 QA (High, 3 pts): Throttle/timeout simulations, credit depletion block, fallback path assertions.

## FE-1 — Onboarding checklist
- User story: As a first-time user, I want a 3-step onboarding checklist and guidance so that I can complete my first optimization quickly.
- Acceptance criteria:
  - Dashboard shows 3-step checklist (Upload resume > Add JD > Optimize & download) with saved progress.
  - Dismissible guidance; "Need guidance?" pill reopens.
  - Completion marks checklist done without blocking navigation.
- Tickets:
  - FE-1 FE (Medium, 2 pts): Checklist component with persistence, dismiss/reopen pill, progress indicators.
  - FE-1 BE (Low, 1 pt): Persist checklist state in user preferences endpoint.
  - FE-1 DB (Low, 1 pt): Add checklist progress fields in preferences JSONB.
  - FE-1 QA (Low, 1 pt): First-time flow, persistence across sessions, dismiss/reopen behavior.

## FE-2 — Dashboard lists and empty states
- User story: As a returning user, I want a dashboard with resume/JD lists, statuses, filters, and quick actions so that I can resume work fast.
- Acceptance criteria:
  - Lists show search/filter, status chips, quick actions (Upload resume, Add JD, New optimization).
  - Item details with consistent CTA placement; empty state encourages upload with privacy copy.
- Tickets:
  - FE-2 FE (High, 3 pts): Dashboard layout with search/filter, cards, empty state hero, quick actions.
  - FE-2 BE (Medium, 2 pts): List endpoints (resumes, JDs, versions) with pagination and status.
  - FE-2 DB (Low, 1 pt): Indexes on status/updated_at for efficient lists.
  - FE-2 QA (Medium, 2 pts): Filters/search, empty state, quick actions navigation smoke tests.

## PERS-1 — Version history
- User story: As a user, I want accepted changes saved as versioned history with timestamps and scores so that I can reuse or re-run them.
- Acceptance criteria:
  - Saved version appears with timestamp, score, status.
  - History supports diff preview side-by-side or unified.
  - Deletion removes version; original resume remains.
- Tickets:
  - PERS-1 FE (Medium, 3 pts): History view with version cards, score badge, diff preview modes.
  - PERS-1 BE (Medium, 3 pts): GET /versions and /versions/{id} with metadata/diff; deletion endpoint.
  - PERS-1 DB (Medium, 2 pts): Version table indexing by user; soft-delete support.
  - PERS-1 QA (Medium, 2 pts): Version creation after save, diff rendering, delete confirmation behavior.

## PERS-2 — Exports (PDF/DOCX/text)
- User story: As a user, I want to preview and export optimized outputs as PDF/DOCX or copy text so that I can submit applications.
- Acceptance criteria:
  - Export modal/controls with spinner/status; download via short-lived signed URL.
  - Export failure shows retry messaging; version remains accessible.
  - Copy text with clear success/fail toasts.
- Tickets:
  - PERS-2 FE (Medium, 2 pts): Export modal/controls with spinner/toast; copy-to-clipboard success state.
  - PERS-2 BE (Medium, 3 pts): POST /exports to trigger PDF/DOCX/text with signed URLs; status polling.
  - PERS-2 DB (Medium, 2 pts): ExportArtifact table; store format and TTL.
  - PERS-2 QA (Medium, 2 pts): Export success/failure retries, signed URL expiry, copy text correctness.

## DEV-1 — CI/CD pipelines
- User story: As a developer, I want CI/CD pipelines across local/staging/prod so that builds, tests, and migrations ship safely.
- Acceptance criteria:
  - CI runs lint/tests/build/migrations; staging deploy applies secrets/flags with health gates; prod rollout runs migrations once with rollback plan.
- Tickets:
  - DEV-1 FE (Medium, 2 pts): CI checks for lint/type/unit; Next.js build pipeline.
  - DEV-1 BE (Medium, 3 pts): FastAPI + worker lint/type/unit/integration; migration runner (Alembic) in pipeline.
  - DEV-1 AI (Medium, 2 pts): Mock provider harness for CI without real calls.
  - DEV-1 DB (Medium, 2 pts): Migration automation with rollback plan; seed for local.
  - DEV-1 QA (Low, 1 pt): Pipeline monitors and release checklist validation.

## DEV-2 — Observability and alerts
- User story: As an operator, I want observability (logs/metrics/traces/alerts) so that I can detect latency, queue, and AI failures.
- Acceptance criteria:
  - Structured logs include requestId/userId, status, latency, error codes.
  - Metrics for optimize/upload/exports (p90/p99 latency, queue depth, AI failures, 5xx).
  - Alerts fire on thresholds with runbook links; health endpoints exposed.
- Tickets:
  - DEV-2 FE (Low, 1 pt): Client-side logging hooks for key events/errors.
  - DEV-2 BE (High, 3 pts): Structured logging middleware, OTel traces/metrics exporters, health endpoints, alerts config.
  - DEV-2 AI (Medium, 1 pt): Provider call tracing and failure tagging.
  - DEV-2 DB (Medium, 2 pts): Audit log table for sensitive access.
  - DEV-2 QA (Low, 1 pt): Observability dashboards verification, synthetic checks on health endpoints.

## QA-1 — E2E/regression coverage
- User story: As QA, I want automated regression/E2E coverage for auth, upload, optimize, and export flows so that releases are stable.
- Acceptance criteria:
  - Nightly E2E passes for auth, upload, JD, optimize, export against staging.
  - Edge cases (invalid files, unverified email, credit gate) block as per UX.
  - Regressions reported with screenshots/logs and tracked to closure.
- Tickets:
  - QA-1 FE (High, 3 pts): Playwright/Cypress E2E scripts for upload > JD > optimize > export.
  - QA-1 BE (Medium, 2 pts): Test data fixtures and mock services for deterministic runs.
  - QA-1 AI (Medium, 1 pt): Stubbed AI responses for deterministic assertions.
  - QA-1 DB (Low, 1 pt): Seed/reset scripts for staging test runs.
  - QA-1 QA (High, 2 pts): Regression suite scheduling, reporting, flake triage.

## QA-2 — Performance and resiliency tests
- User story: As QA, I want performance and resiliency tests for the optimization pipeline so that p90 latency and retry behavior stay within targets.
- Acceptance criteria:
  - Load tests for 500 concurrent optimizations keep p90 <=20s within retry tolerance.
  - Provider throttling exercises retry/backoff; error codes surfaced without crashes.
  - Chaos tests on queue/worker restarts recover or fail gracefully with status updates.
- Tickets:
  - QA-2 BE (High, 3 pts): Load/perf test scripts hitting optimize queue, measuring p90/p99.
  - QA-2 AI (High, 2 pts): Stress test adapter with throttling and retry scenarios.
  - QA-2 DB (Medium, 2 pts): Monitor query performance under load; add indexes if needed.
  - QA-2 QA (High, 2 pts): Chaos/resiliency playbook and reports on latency/error budgets.
