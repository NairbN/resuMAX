# resuMAX — Sprint Backlog (MVP)

## 1. Overview
This sprint delivers the end-to-end MVP: verified users can upload resumes and job descriptions, run AI-powered optimizations with diff control, view statuses/history, and export optimized outputs, backed by secure auth, durable storage, resilient queues, observability, and test coverage that matches the documented UX flows and system architecture.

---

## 2. Epics Table
| Epic | Description | Priority (High/Medium/Low) |
| --- | --- | --- |
| Auth & Account Management | Email/password auth, verification, password reset, profile | High |
| Resume Upload & Storage | Resume ingest, validation, parsing status, storage lifecycle | High |
| Job Description Upload & Storage | JD paste/upload, metadata capture, pairing readiness | High |
| Optimization Engine Integration | AI orchestration, diff/rewrite, retries/timeouts/credits | High |
| Frontend UI & Flows | Onboarding checklist, dashboard lists, navigation and states | High |
| Persistence & Saved Results | Versions/history, exports (PDF/DOCX/text), download URLs | High |
| Deployment & DevOps | CI/CD, environments, infrastructure as code, observability | Medium |
| QA & Test Coverage | E2E/regression, performance/latency, AI reliability tests | High |

---

## 3. User Stories
### Auth & Account Management
- **AUTH-1** As a job seeker, I want to sign up, verify my email, and log in so that I can securely access the dashboard.
- **AUTH-2** As a user, I want to reset my password and manage my profile so that I can regain access and keep my account current.

### Resume Upload & Storage
- **RES-1** As a job seeker, I want to upload my resume (PDF/DOCX <=5 MB) and see parse status so that I know it is ready for optimization.
- **RES-2** As a job seeker, I want to view, rename, or delete my uploaded resumes with clear statuses so that I can manage my library.

### Job Description Upload & Storage
- **JD-1** As a job seeker, I want to paste or upload a job description (<=10 MB) with title/company/location so that it is labeled for pairing.
- **JD-2** As a job seeker, I want to pair a JD to a resume and see validation so that I can start optimization confidently.

### Optimization Engine Integration
- **OPT-1** As a job seeker, I want to run optimization with summary, diff, and apply-all/per-change controls so that I can tailor my resume safely.
- **OPT-2** As a user, I want reliable optimization with retries, timeout handling, and credit gating (when enabled) so that I am not blocked by failures.

### Frontend UI & Flows
- **FE-1** As a first-time user, I want a 3-step onboarding checklist and guidance so that I can complete my first optimization quickly.
- **FE-2** As a returning user, I want a dashboard with resume/JD lists, statuses, filters, and quick actions so that I can resume work fast.

### Persistence & Saved Results
- **PERS-1** As a user, I want accepted changes saved as versioned history with timestamps and scores so that I can reuse or re-run them.
- **PERS-2** As a user, I want to preview and export optimized outputs as PDF/DOCX or copy text so that I can submit applications.

### Deployment & DevOps
- **DEV-1** As a developer, I want CI/CD pipelines across local/staging/prod so that builds, tests, and migrations ship safely.
- **DEV-2** As an operator, I want observability (logs/metrics/traces/alerts) so that I can detect latency, queue, and AI failures.

### QA & Test Coverage
- **QA-1** As QA, I want automated regression/E2E coverage for auth, upload, optimize, and export flows so that releases are stable.
- **QA-2** As QA, I want performance and resiliency tests for the optimization pipeline so that p90 latency and retry behavior stay within targets.

---

## 4. Acceptance Criteria
- **AUTH-1**
  - Given an unverified signup, When I attempt to upload, Then I see a blocking banner with "Resend verification" and uploads are disabled.
  - Given valid credentials, When I log in, Then I receive access/refresh tokens and land on the dashboard.
  - Given an invalid login, When I submit, Then the UI shows inline error without clearing inputs and rate limits excessive attempts.
  - Given a verified account, When I refresh tokens, Then session persists without re-login until expiry.
- **AUTH-2**
  - Given I forgot my password, When I request reset, Then an email with a time-bound token is sent and rate limited.
  - Given a valid reset token, When I set a new strong password, Then I can log in and prior sessions are revoked.
  - Given I update profile fields, When I save, Then changes persist and reflect on reload.

- **RES-1**
  - Given a PDF/DOCX <=5 MB, When I drop it in the uploader, Then client validates type/size and shows progress with cancel.
  - Given upload success, When parsing completes, Then I see detected sections summary and status chip updates to completed.
  - Given parsing fails, When the job errors, Then an inline banner shows retry guidance and the file remains available to retry.
  - Given an unsupported file/size, When I attempt upload, Then the CTA stays disabled and inline validation shows the rule.
- **RES-2**
  - Given resumes exist, When I open the dashboard, Then I see cards with status (pending/parsing/completed/failed), timestamps, and rename/delete actions.
  - Given I rename a resume, When I confirm, Then the new title persists and reflects in selectors.
  - Given I delete a resume, When I confirm, Then the record is soft-deleted and hidden from lists with storage cleanup triggered.

- **JD-1**
  - Given I paste or upload JD text/PDF/DOCX <=10 MB, When I save, Then the system sanitizes text and extracts/lets me edit title/company/location.
  - Given metadata is missing, When I try to save, Then I am prompted to add a title before proceeding.
  - Given upload failure, When it occurs, Then my pasted text persists and I can retry without retyping.
- **JD-2**
  - Given I have at least one resume and JD, When I select both, Then validation confirms pairing readiness before enabling Optimize.
  - Given selections are invalid or missing, When I click Optimize, Then the CTA is disabled with inline guidance.
  - Given pairing saved, When I return, Then the previous selection is remembered for quick re-run.

- **OPT-1**
  - Given a paired resume/JD and credits (if enabled), When I start optimization, Then status chips show queued > processing > generating with "<20s typical" hint.
  - Given AI output returns, When I view the preview, Then I see summary, alignment score, and diff with accept-all/per-change toggles.
  - Given I accept or reject changes, When I save, Then a version is created with accepted changes captured for audit.
  - Given AI flags uncertain content, When shown, Then original text is selected by default with warning copy.
- **OPT-2**
  - Given an optimization timeout or 429, When it happens, Then the job retries up to 2 times before marking failed with user-facing error.
  - Given provider failure, When fallback is configured, Then the adapter routes to secondary provider before failing.
  - Given credit balance is zero (flag on), When I click Optimize, Then a modal gates the action and links to Billing.
  - Given a job fails, When I retry, Then previous selections persist and status resets appropriately.

- **FE-1**
  - Given a new user, When I land on dashboard, Then I see a 3-step checklist (Upload resume > Add JD > Optimize & download) with progress saved.
  - Given I dismiss guidance, When I need it again, Then a "Need guidance?" pill reopens the checklist.
  - Given I complete steps, When done, Then the checklist marks complete and does not block navigation.
- **FE-2**
  - Given resumes/JDs exist, When I open dashboard, Then lists show search/filter, status chips, and quick actions (Upload resume, Add JD, New optimization).
  - Given an item is selected, When I view it, Then details and actions (rename/delete/open) are available with consistent CTA placement.
  - Given no data, When I land, Then an empty state hero encourages upload with privacy reassurance copy.

- **PERS-1**
  - Given I save accepted changes, When processing completes, Then a version with timestamp, score, and status appears in history.
  - Given multiple versions, When I open history, Then I can preview diffs side-by-side or unified.
  - Given a deletion request, When confirmed, Then the version is removed while original resume remains.
- **PERS-2**
  - Given a saved version, When I choose export, Then I can download PDF/DOCX or copy text with clear success/fail toasts.
  - Given export generation, When in progress, Then a spinner and status are shown; on completion, download link uses a short-lived signed URL.
  - Given export failure, When it occurs, Then I see retry messaging and the version remains accessible.

- **DEV-1**
  - Given code is pushed, When CI runs, Then lint/tests/build and migrations execute with blocking failures on errors.
  - Given staging deploy, When triggered, Then env secrets/feature flags are applied and health checks gate promotion.
  - Given prod deploy, When rolled out, Then migrations are run once with rollback plan and status reported.
- **DEV-2**
  - Given services run, When requests occur, Then structured logs include requestId/userId, status, latency, and error codes.
  - Given metrics pipeline, When optimize/upload/exports run, Then p90/p99 latency, queue depth, AI failures, and 5xx rates are emitted to dashboards.
  - Given alert thresholds, When exceeded (e.g., AI failure rate, queue backlog), Then alerts fire to on-call with runbook links.

- **QA-1**
  - Given nightly runs, When E2E executes, Then auth, upload, JD, optimize, and export happy-paths pass against staging.
  - Given edge cases (invalid files, unverified email, credit gate), When tested, Then UI blocks and error messages match UX spec.
  - Given regressions, When found, Then failures are reported with screenshots/logs and tracked to closure.
- **QA-2**
  - Given load tests, When 500 concurrent optimizations are simulated, Then p90 latency stays <=20s and failures are within retry tolerance.
  - Given AI retries, When providers throttle, Then retry/backoff logic is exercised and error codes surfaced without crashing workers.
  - Given chaos tests on queue/worker restarts, When performed, Then jobs recover or fail gracefully with user-facing status updates.

---

## 5. Task Breakdown
- **AUTH-1**
  - FE: Build signup/login forms with inline validation, verification banner gating uploads [3 points] [High]
  - BE: Implement register/login/refresh/verify endpoints in FastAPI with Pydantic validation, rate limits, and JWT issuance [5 points] [High]
  - AI: Not applicable [0 points] [Low]
  - DB: Create user + verification token schema/migration; add indices on email [3 points] [High]
  - QA: Auth happy/invalid paths, unverified upload block, token refresh tests [3 points] [High]

- **AUTH-2**
  - FE: Password reset request/confirm screens with password rules; profile edit form [3 points] [Medium]
  - BE: Password reset request/confirm endpoints, token expiry, session revocation [3 points] [High]
  - AI: Not applicable [0 points] [Low]
  - DB: Add password reset token table/fields; audit profile updates [2 points] [Medium]
  - QA: Reset flow tests, strength rules, profile persistence regression [2 points] [Medium]

- **RES-1**
  - FE: Resume upload dropzone with type/size checks, progress, cancel, parse status display [3 points] [High]
  - BE: POST /resumes/presign and /resumes/{id}/parse FastAPI routers with Pydantic validation, presigned URLs, and Celery/Dramatiq parse job enqueue [3 points] [High]
  - AI: Not applicable [0 points] [Low]
  - DB: Resume table migration (fields per architecture) via Alembic/SQLAlchemy; indexes for status [3 points] [High]
  - QA: Upload/parse success, invalid file/size, parse failure retry coverage; verify worker status updates [2 points] [High]

- **RES-2**
  - FE: Dashboard cards/list with status chips, rename/delete overflow menu, timestamps [2 points] [Medium]
  - BE: PATCH/DELETE resume endpoints in FastAPI with ownership checks, soft-delete, and storage cleanup job enqueue [3 points] [Medium]
  - AI: Not applicable [0 points] [Low]
  - DB: Deleted_at handling, triggers or Celery task kickoff for storage cleanup [2 points] [Medium]
  - QA: Rename/delete flows, status rendering, soft-delete isolation tests [2 points] [Medium]

- **JD-1**
  - FE: JD paste/upload UI with sanitization note, metadata inputs, sticky save CTA [2 points] [High]
  - BE: POST /job-descriptions with sanitize/extract implemented in FastAPI; enforce size/type limits and storage handling [3 points] [High]
  - AI: Light metadata extraction prompt fallback for missing title/company (worker task) [1 point] [Low]
  - DB: JD table migration with sanitized_text and metadata JSONB [2 points] [High]
  - QA: Missing title block, paste preservation on failure, metadata extraction accuracy smoke tests [2 points] [Medium]

- **JD-2**
  - FE: Pairing selector UI with validation copy and disabled Optimize until valid [2 points] [High]
  - BE: Pairing validation in optimize request; persist last selected resume/JD in FastAPI [2 points] [Medium]
  - AI: Not applicable [0 points] [Low]
  - DB: Store last_selected_resume_id/jd_id in user preferences [1 point] [Low]
  - QA: Pairing validation, remembered selection on return, invalid selection errors [2 points] [Medium]

- **OPT-1**
  - FE: Optimization workspace with status chips, summary panel, diff (side-by-side/unified), accept-all/per-change toggles, sticky footer [5 points] [High]
  - BE: POST /optimize enqueue, GET status payload with summary/diff, POST accept changes to create version in FastAPI; enqueue optimize job to Celery/RQ [5 points] [High]
  - AI: Build prompt templates (summary/gap/rewrite), schema validation, conservative tone, uncertainty flagging executed in worker [5 points] [High]
  - DB: OptimizationRequest and OptimizationVersion migrations; store diffs/accepted_changes JSONB [3 points] [High]
  - QA: End-to-end optimize flow, diff correctness, accept-all/per-change persistence, uncertainty warnings [3 points] [High]

- **OPT-2**
  - FE: Error/timeout handling UI ("Still working???", retry, email me), credit gate modal (feature-flag) [3 points] [High]
  - BE: Retry/backoff logic in Celery/SQS, provider fallback, credit check before enqueue, error codes surfaced to client [4 points] [High]
  - AI: Provider adapter with fallback routing, deterministic validation, capped tokens [3 points] [High]
  - DB: Credit ledger (flagged), error_code/message fields on optimization jobs [2 points] [Medium]
  - QA: Throttle/timeout simulations, credit depletion block, fallback path assertions [3 points] [High]

- **FE-1**
  - FE: Checklist component with persistence, dismiss/reopen pill, progress indicators [2 points] [Medium]
  - BE: Persist checklist state in user preferences endpoint [1 point] [Low]
  - AI: Not applicable [0 points] [Low]
  - DB: Add checklist progress fields in preferences JSONB [1 point] [Low]
  - QA: First-time flow, persistence across sessions, dismiss/reopen behavior [1 point] [Low]

- **FE-2**
  - FE: Dashboard layout with search/filter, cards, empty state hero, quick actions [3 points] [High]
  - BE: List endpoints (resumes, JDs, versions) with pagination and status [2 points] [Medium]
  - AI: Not applicable [0 points] [Low]
  - DB: Indexes on status/updated_at for efficient lists [1 point] [Low]
  - QA: Filters/search, empty state, quick actions navigation smoke tests [2 points] [Medium]

- **PERS-1**
  - FE: History view with version cards, score badge, diff preview modes [3 points] [Medium]
  - BE: GET /versions and GET /versions/{id} returning metadata/diff, deletion endpoint [3 points] [Medium]
  - AI: Not applicable [0 points] [Low]
  - DB: Version table indexing by user, soft-delete support [2 points] [Medium]
  - QA: Version creation after save, diff rendering, delete confirmation behavior [2 points] [Medium]

- **PERS-2**
  - FE: Export modal/controls with spinner/toast, copy-to-clipboard with success state [2 points] [Medium]
  - BE: POST /exports to trigger PDF/DOCX/text with signed URLs; status polling [3 points] [Medium]
  - AI: Not applicable [0 points] [Low]
  - DB: ExportArtifact table; store format and TTL [2 points] [Medium]
  - QA: Export success/failure retries, signed URL expiry, copy text correctness [2 points] [Medium]

- **DEV-1**
  - FE: CI checks for lint/type/unit; build pipeline for Next.js [2 points] [Medium]
  - BE: CI checks for FastAPI + worker lint/type/unit/integration with pytest; migration runner (Alembic) in pipeline [3 points] [Medium]
  - AI: Mock provider harness for CI without real calls [2 points] [Medium]
  - DB: Migration automation with rollback plan and seed for local [2 points] [Medium]
  - QA: Pipeline monitors and release checklist validation [1 point] [Low]

- **DEV-2**
  - FE: Client-side logging hooks for key events/errors [1 point] [Low]
  - BE: Structured logging middleware (structlog/loguru), OpenTelemetry traces/metrics exporters, health endpoints, alerts config [3 points] [High]
  - AI: Provider call tracing and failure tagging [1 point] [Medium]
  - DB: Audit log table for access to sensitive records [2 points] [Medium]
  - QA: Observability dashboards verification, synthetic checks on health endpoints [1 point] [Low]

- **QA-1**
  - FE: Playwright/Cypress E2E scripts for upload > JD > optimize > export [3 points] [High]
  - BE: Test data fixtures and mock services for deterministic runs [2 points] [Medium]
  - AI: Stubbed AI responses for deterministic assertions [1 point] [Medium]
  - DB: Seed/reset scripts for staging test runs [1 point] [Low]
  - QA: Regression suite scheduling, reporting, and flake triage [2 points] [High]

- **QA-2**
  - FE: None beyond instrumentation for timing capture [0 points] [Low]
  - BE: Load/perf test scripts hitting optimize queue, measuring p90/p99 (FastAPI + worker) [3 points] [High]
  - AI: Stress test adapter with throttling and retry scenarios [2 points] [High]
  - DB: Monitor query performance under load; add indexes if needed [2 points] [Medium]
  - QA: Chaos/resiliency playbook and reports on latency/error budgets [2 points] [High]
## 6. Sprint Kanban View
### To Do
- AUTH-1 FE/BE/DB/QA, AUTH-2 FE/BE/DB/QA
- RES-1 FE/BE/DB/QA, RES-2 FE/BE/DB/QA
- JD-1 FE/BE/AI/DB/QA, JD-2 FE/BE/DB/QA
- OPT-1 FE/BE/AI/DB/QA, OPT-2 FE/BE/AI/DB/QA
- FE-1 FE/BE/DB/QA, FE-2 FE/BE/DB/QA
- PERS-1 FE/BE/DB/QA, PERS-2 FE/BE/DB/QA
- DEV-1 FE/BE/AI/DB/QA, DEV-2 FE/BE/AI/DB/QA
- QA-1 FE/BE/AI/DB/QA, QA-2 BE/AI/DB/QA

### In Progress
- (empty)

### Done
- (empty)

---

## 7. Dependencies & Risks
- Upload and parse flows depend on presigned URL generation, storage availability, and parsing worker readiness.
- Optimization requires validated resume/JD pairing, credit check (if enabled), and AI provider availability; retries/fallback must be in place before enabling user access.
- Export flows depend on completed versions and headless rendering; ensure queue capacity and signed URL correctness.
- Auth/verification gating must ship before enabling uploads to prevent unverified data ingestion.
- Observability and alerting should precede public traffic to catch AI/queue/storage failures early.
- Performance risk: AI latency and queue backlog could breach 20s target; mitigate with autoscale and parallel section generation.
- Privacy/security risk: tenancy checks and signed URL scoping must be enforced before launch.

---

## 8. Out of Scope for MVP
- Cover letter generation, ATS scoring reports, LinkedIn import, and collaboration/sharing links.
- Native mobile apps and browser extensions.
- Multi-language optimization beyond English.
- Advanced analytics dashboards for recruiters or users.
- Direct ATS/job board submissions.

---

## 9. Backlog Health Check
- Epics cover auth, uploads, optimization, exports, history, DevOps, and QA as per BRD/architecture.
- User stories map to documented UX flows with edge/error handling and privacy cues.
- Acceptance criteria include UI states, API behaviors, validation, and persistence expectations.
- Tasks span FE/BE/AI/DB/QA with sizing and priority to guide sprint planning.
- Dependencies highlight queue/AI/storage readiness before exposing optimization.
- Observability and performance tasks align with 20s p90 latency and 99.5% uptime goals.
- Security controls (verification, tenancy, signed URLs) are embedded in early stories.
- Out-of-scope list preserves MVP focus and prevents scope creep.
- QA coverage includes E2E, regression, and perf/resiliency to reduce release risk.
- CI/CD and environment readiness ensure staging/prod parity for reliable releases.
