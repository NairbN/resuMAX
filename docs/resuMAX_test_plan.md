# resuMAX — QA Test Plan (MVP)

## 1. Purpose & Scope
- Provide end-to-end QA coverage for the resuMAX MVP web app, validating core flows: auth, onboarding, resume upload/parsing, JD intake, pairing, AI optimization, diff/acceptance, version history, and exports (PDF/DOCX/text).
- In scope: UI/UX compliance with design system, API/worker/storage/AI integrations, credit gating (when enabled), error/retry handling, data integrity/persistence, observability signals, and basic performance aligned to the 20s p90 target.
- Out of scope for this plan: native mobile apps, collaboration/sharing, cover letters/ATS scoring/LinkedIn import, multi-language generation, advanced analytics, deep security/pen testing, and heavy-load stress beyond MVP targets.

## 2. Test Objectives
- Validate all core user flows (onboarding, upload, optimization, save/export, history).
- Verify AI optimization behaves reliably, returns truthful, ATS-friendly results, and surfaces uncertainty warnings with safe defaults.
- Confirm data persistence, integrity, tenancy isolation, and retrieval across sessions.
- Ensure UX/UI alignment with UX flows and design system (layout, states, copy, accessibility basics, responsiveness).
- Verify error handling, validation, retry, and messaging for uploads, optimization, exports, and auth.
- Exercise API contracts and integrations (auth, presign, parse, optimize, versions, exports, billing flag) with positive/negative cases.
- Protect privacy and security fundamentals (verification gating, signed URLs, access control).

## 3. Test Approach & Methodology
- Functional testing: user-story-based coverage for auth, uploads, pairing, optimization, history, exports, billing gate, onboarding checklist; includes happy, negative, and boundary cases.
- Integration testing: front-end to API to queue/worker/storage/AI; verify status polling/websocket/SSE updates; validate signed URLs and storage artifacts.
- UI/UX validation: compare against UX spec and design system (states, spacing, typography, color tokens, focus rings, sticky footers, toasts, diff/preview modes, checklist behavior); verify copy from UX writing examples.
- API testing: contract and validation for `/auth/*`, `/resumes/presign`, `/resumes/{id}/parse`, `/job-descriptions`, `/optimize`, `/optimize/{id}`, `/optimize/{id}/accept`, `/versions`, `/exports`, `/billing/credits` (flagged). Include ownership checks and rate limits.
- AI response validation: schema/format adherence, alignment score present, conservative tone, no hallucinated entities (compare to parsed resume), uncertainty warnings default to original text, retries/backoff, fallback provider coverage, capped latency.
- Regression: smoke on each build; nightly automated E2E (upload > JD > optimize > export) using mock AI for determinism plus selective real-provider staging runs; check checklist persistence and navigation guards.
- Cross-browser/device: latest Chrome, Edge, Safari; responsive behavior at desktop/tablet/mobile breakpoints; keyboard navigation basics.
- Data/resiliency: simulate network interruption, retry flows, token refresh, signed URL expiry, queue retry visibility; verify idempotency on optimize/export.

## 4. Test Environment
- Local: Next.js + FastAPI with Docker (PostgreSQL, Redis/MinIO); mock AI provider; seeded users (verified/unverified, credit states, admin) and sample resumes/JDs.
- Staging: Prod-parity topology with sandbox AI keys, email service enabled (verification/reset), signed URLs to staging storage, TLS, feature flags toggleable (credits gate, fallback provider, checklist), observability dashboards and logs accessible.
- Pre-prod (if used): Same as staging with production-like data retention and real AI keys for final verification; restricted access.
- Test accounts & data: at least one verified user, one unverified, zero-credit user, credit-sufficient user, admin; seeds for resumes/JDs/versions; tokens for password reset/verification tests.
- Configuration/flags: credits on/off, fallback AI provider, mock AI enablement, checklist enablement, email verification enforcement, export formats enabled, SSE/websocket status updates.
- External dependencies: AI providers (OpenAI/Anthropic), object storage (S3/MinIO), queue (Redis/SQS), email service, optional payment processor; ensure sandbox keys and TTLs configured.
- Test code locations: frontend tests in `apps/frontend/tests/*`, backend tests in `apps/api/tests/*`, worker tests in `apps/worker/tests`, E2E suites in `tests/e2e`, API contract tests in `tests/contracts`, shared fixtures in `tests/fixtures` (see docs/resuMAX_file_structure.md).

## 5. Key User Journeys to Validate
- New user sign-up and initial login: ensures verification gating, checklist visibility, secure session start.
- Returning user login: confirms session persistence/refresh, history retrieval, and dashboard readiness.
- Uploading a resume: validates file rules, parsing pipeline, status badges, privacy cues.
- Uploading a job description: validates paste/upload, sanitization, metadata capture, and pairing readiness.
- Running optimization and viewing results: covers pairing validation, credit check, status chips/stepper, summary + diff, accept-all/per-change controls, uncertainty warnings.
- Saving and downloading optimized resumes: confirms version creation, preview, export to PDF/DOCX/text, copy to clipboard, and history updates.
- Viewing previously saved optimizations: ensures history cards, status/score, diff preview, re-download/re-run paths.

## 6. Feature-Based Test Coverage (Mapped to Epics)
### Epic: Auth & Account Management
- Description: Email/password auth with verification, session refresh, password reset, profile updates.
- Coverage:
  - Sign-up/login validation, rate limiting, focus/disabled/loading states per design system.
  - Verification gating before uploads; resend verification flow.
  - Token refresh, logout, session expiry handling.
  - Password reset (request/confirm), strong password rules, session revocation after reset.
  - Profile update persistence; ownership/authorization checks; privacy copy present.

### Epic: Resume Upload & Storage
- Description: Upload, parse, store, manage resumes with statuses.
- Coverage:
  - Drag-drop/picker, PDF/DOCX acceptance, 5 MB limit, inline errors, disable CTA while invalid.
  - Upload progress, cancel, retry behavior; privacy tooltip and rules copy.
  - Parse success with section summary; parse failure banner with retry/re-run parse.
  - Status chips (pending/parsing/completed/failed) alignment to backend states.
  - Rename/delete with confirmation; soft delete isolation; signed URL scoping and tenancy checks.

### Epic: Job Description Upload & Storage
- Description: Paste/upload JD, sanitize, capture metadata, prepare for pairing.
- Coverage:
  - Paste + file upload (PDF/DOCX/text) up to 10 MB; sanitization note visible.
  - Metadata extraction/edit (title/company/location); block save when title missing.
  - Persisted JD list with labels; pairing prompts; error retries preserving pasted text.
  - Storage isolation and signed URL scoping for uploaded JDs.

### Epic: Optimization Engine Integration
- Description: Orchestrate AI optimization with reliability, controls, and credit gating.
- Coverage:
  - Pairing validation before enabling Optimize; remembered selections.
  - Status chips/stepper (queued > processing > generating > ready) with "<20s typical" hint.
  - Credit balance check/modal gating when flag on; correct deduction on optimize start.
  - Summary panel, alignment score, diff views (side-by-side/unified), accept-all/per-change toggles, uncertainty warnings defaulting to original text.
  - Retry/backoff on timeout/429; fallback provider routing; clear error codes/messages; idempotent retries without double-charging credits.
  - Audit of accepted changes stored; logging of job lifecycle.

### Epic: Frontend UI & Flows
- Description: Dashboard, onboarding checklist, navigation, states.
- Coverage:
  - 3-step checklist (Upload resume > Add JD > Optimize & download), persistence across sessions, dismiss/reopen via pill.
  - Dashboard lists with search/filter, status badges, timestamps, score; empty state hero with privacy reassurance.
  - Navigation guards for unsaved changes; sticky footers; toasts/banners; focus rings per design system; responsive layouts desktop/tablet/mobile.
  - Latency notice/help links; credit badge and profile/help menus.

### Epic: Persistence & Saved Results
- Description: Version history, diff review, exports, deletion.
- Coverage:
  - Version creation after accept/save; timestamp, score, status chips; side-by-side/unified diff preview.
  - Re-run optimization using stored resume/JD; history list ordering and pagination.
  - Export PDF/DOCX/text with spinner/toasts; signed URL validity/expiry; copy-to-clipboard success.
  - Rename/delete versions with confirmation; audit trail notes; ensure originals remain.

### Epic: Deployment & DevOps
- Description: CI/CD, environment readiness, observability.
- Coverage:
  - CI pipelines run lint/tests/build/migrations; failures block deploy.
  - Health checks for API/workers/storage; feature flags set per env.
  - Structured logs/metrics/traces emitted (requestId, latency, error codes, queue depth); alerts for AI failure rate/queue backlog/storage errors.
  - Backup/rollback plan for migrations; mock AI wired for CI.

### Epic: QA & Test Coverage
- Description: Automation and reliability testing to protect MVP flows.
- Coverage:
  - Playwright/Cypress E2E for auth > upload > JD > optimize > export; deterministic mock AI fixtures.
  - Nightly regression schedule with flake triage; screenshot/log capture; staging data reset scripts.
  - Performance smoke for optimize latency (p90 <=20s target) and retry behavior under throttling; chaos tests for worker restarts.
  - Traceability matrix maintained linking stories/acceptance criteria to tests.

## 7. Detailed Test Cases
### Test Case: TC-AUTH-1 New signup with verification gating
User Story Reference: AUTH-1  
Prerequisites:
- Fresh email inbox or mail catcher; verification required flag enabled.

Steps:
1. Sign up with valid email/strong password.
2. Land on dashboard; observe 0/3 checklist and verification banner.
3. Attempt resume upload before verifying.
4. Click "Resend verification" and complete verification via emailed token/link.
5. Retry upload after verification.

Expected Result:
- Tokens issued; uploads blocked until verified; resend link works; banner clears after verification; checklist persists progress.

Edge Cases:
- Invalid email format blocked client-side; repeated resend attempts rate limited; session refresh preserves gating.

### Test Case: TC-AUTH-2 Password reset and profile update
User Story Reference: AUTH-2  
Prerequisites:
- Verified user account; access to reset email.

Steps:
1. Trigger password reset request; capture email with time-bound token.
2. Submit new strong password; ensure prior sessions revoked.
3. Log in with new password.
4. Update profile fields (name, preferences) and save.

Expected Result:
- Reset token validated; weak passwords rejected; login works with new credentials; profile changes persist across reload.

Edge Cases:
- Expired/used token blocked with guidance; reset attempts rate limited; verify no session fixation.

### Test Case: TC-RES-1 Resume upload, parse, and status rendering
User Story Reference: RES-1  
Prerequisites:
- Verified logged-in user; valid PDF <=5 MB.

Steps:
1. Open Upload Resume; drag-drop file.
2. Observe inline validation, privacy note, and disabled CTA until valid.
3. Confirm upload progress bar with cancel; allow parse to complete.
4. View detected section summary and status chip changing to completed.
5. Rename resume from overflow menu.

Expected Result:
- Upload accepted; progress and statuses display correctly; sections shown; rename persists; storage key associated to user.

Edge Cases:
- >5 MB or unsupported type blocked with inline error; cancel stops upload; parse failure shows retry banner and preserves file card; re-run parse updates status.

### Test Case: TC-JD-1 Job description paste/upload with metadata
User Story Reference: JD-1  
Prerequisites:
- At least one resume available.

Steps:
1. Add JD via paste text; observe sanitization note.
2. Confirm auto-extracted title/company/location; edit fields.
3. Save JD; view JD list entry.
4. Upload JD file (PDF/DOCX/text) within size limit.

Expected Result:
- Save blocked until title present; sanitized text stored; metadata editable/persisted; JD appears with label.

Edge Cases:
- Upload failure preserves pasted text; missing metadata prompts inline error; >10 MB rejected with helper copy.

### Test Case: TC-JD-2 Pairing validation and optimize happy path
User Story Reference: JD-2, OPT-1  
Prerequisites:
- One parsed resume, one saved JD; credits available (if enabled); verified user.

Steps:
1. Start new optimization; select resume + JD.
2. Observe Optimize CTA disabled until valid pairing.
3. Click Optimize; watch status chips/stepper transitions with "<20s typical" hint.
4. When ready, review summary, alignment score, diff (side-by-side/unified).
5. Accept some changes individually, then Apply All; Save version.

Expected Result:
- Optimize runs once; statuses accurate; summary/diff align to inputs; accept-all/per-change controls persist choices; version created with audit of accepted changes.

Edge Cases:
- Change selection mid-process blocked; navigate away prompts unsaved changes; UI shows uncertainty warnings defaulting to original text.

### Test Case: TC-OPT-2 Timeout/retry/fallback behavior
User Story Reference: OPT-2  
Prerequisites:
- Ability to simulate AI timeout/429; credits available; fallback provider enabled.

Steps:
1. Trigger optimization while throttling primary provider.
2. Observe retries (max 2) and fallback provider attempt.
3. If still failing, view error banner/toast with guidance and preserved selections.
4. Retry optimization after failure.

Expected Result:
- Retries logged; fallback invoked; no duplicate credit deduction; status transitions to failed then resets on retry; user-facing message clear.

Edge Cases:
- Timeout exceeds budget shows "Still working... <5s more" then fallback CTA "Email me when ready"; verify email queued if used.

### Test Case: TC-CREDIT-1 Credit gate modal (feature-flagged)
User Story Reference: OPT-2  
Prerequisites:
- Credits feature on; user with zero balance.

Steps:
1. Attempt Optimize with zero credits.
2. Observe modal gating action with link to Billing.
3. Add credits (or admin grant); re-attempt Optimize.

Expected Result:
- Optimize blocked until credits sufficient; modal copy matches UX spec; balance decremented exactly once on start.

Edge Cases:
- Balance refresh latency handled; gate respects multiple tabs; copy text export still allowed if permitted.

### Test Case: TC-PERS-1 Save version, history, and exports
User Story Reference: PERS-1, PERS-2  
Prerequisites:
- Completed optimization result.

Steps:
1. Accept/reject changes and Save version.
2. Open history; verify card shows timestamp, score, status; preview diff (side-by-side/unified).
3. Export PDF and DOCX; copy text.
4. Re-download via history list; delete version with confirmation.

Expected Result:
- Version stored with correct metadata; exports succeed with signed URLs; copy text matches optimized content; delete removes version but keeps original resume.

Edge Cases:
- Export failure shows retry toast; expired signed URL triggers reissue; deletion requires confirmation.

### Test Case: TC-FE-1 Onboarding checklist and dashboard UX
User Story Reference: FE-1, FE-2  
Prerequisites:
- New account (no data).

Steps:
1. Land on dashboard empty state; view hero copy and checklist (0/3).
2. Complete Upload resume, Add JD, Optimize steps; observe checklist progress.
3. Dismiss checklist; reopen via "Need guidance?" pill.
4. Validate dashboard search/filter, status chips, quick actions; test responsive layout (desktop/tablet/mobile widths).

Expected Result:
- Checklist persists across reloads; completion does not block navigation; empty and populated states match spec; responsive layout reflows without broken controls.

Edge Cases:
- Email unverified blocks upload with banner; filters handle no results gracefully; focus states visible for keyboard users.

## 8. Negative & Edge Case Testing
- Unsupported or corrupted files (resume >5 MB, JD >10 MB, wrong mime): block upload, show inline error, keep file card for retry.
- Missing required fields (JD title, auth inputs, password rules): disable CTAs with inline validation; preserve user input.
- Unverified email attempting upload/optimize: blocking banner with resend link; action disabled.
- AI service timeout/failure/throttle: retries/backoff, fallback provider, clear error codes, preserved selections, optional email when ready.
- Network interruption mid-upload/optimization/export: show failure toast, allow retry without clearing selections; ensure idempotent retries.
- User refresh/back navigation during optimization or unsaved changes: warning modal; status persists after reload.
- Credit depletion mid-flow (flag on): gate optimize, prevent double charges, surface balance pill.
- Signed URL expiry or unauthorized access: return 403/expired message; ensure other users cannot access artifacts.
- Empty states: no resumes/JDs/versions display guided empty cards with privacy reassurance.

## 9. Acceptance Criteria Cross-Check
- Maintain a traceability matrix linking each user story and acceptance criterion from the sprint backlog to one or more test cases (manual or automated).
- For each story, verify both functional behavior and UX/UI expectations (states, copy, accessibility basics) match UX/UI spec and design system.
- Mark acceptance when criteria pass in staging with evidence (screenshots/logs/export artifacts); regress after fixes.
- Use checklist for edge cases specified in acceptance criteria (e.g., unverified upload block, retry behavior, signed URL gating).

## 10. Non-Functional Testing
- Performance: monitor optimization latency (target p90 <=20s, p99 <=30s), upload/parse latency, export turnaround; basic load test around expected concurrency; verify queue depth under load.
- Security: auth/authorization checks on every resource, tenancy isolation for resumes/JDs/versions, TLS enforced, signed URL TTLs, rate limits, no sensitive data in logs.
- Reliability: queue retry limits, idempotency of optimize/export, resume/JD storage durability, status polling/WebSocket resilience.
- Privacy: ensure PII redaction in logs, access audit trails for sensitive actions, soft-delete behavior, account deletion data cleanup readiness.
- Accessibility: keyboard navigation through forms, visible focus states, ARIA labels for inputs/buttons, color contrast in key components, skip-to-content if available.
- Responsiveness: layout reflows for desktop/tablet/mobile per design system breakpoints; sticky actions usable on mobile.

## 11. Test Data Strategy
- Resumes: varied industries (tech, healthcare, finance), lengths (1-4 pages), formats (clean DOCX, PDF with tables/columns), edge samples (heavily formatted PDF, light text resumes).
- Job descriptions: multiple roles/seniority, long-form and concise, with/without metadata; include noisy formatting for sanitization checks.
- Synthetic/anonymized data to avoid real PII; generate corrupted/oversized files for negative tests.
- AI-specific sets: resumes with missing keywords to validate gap analysis; cases with similar wording to test hallucination guardrails; deterministic mock AI outputs for automation.
- Credit states: seed accounts with zero, low, and ample credits; version history seeds for re-run scenarios.

## 12. Defect Management & Reporting
- Tooling: log defects in the team issue tracker with template requiring environment, build version, story/epic link, steps, expected vs actual, screenshots/video, console/network logs, and data samples.
- Severity/Priority: Blocker (core flow broken/security), Critical (major function failure/no workaround), Major (function impaired with workaround), Minor (cosmetic/content).
- Triage: QA lead and PM review daily; assign owner; set fix version; confirm repro steps and scope.
- Retest & regression: verify fixes in staging, rerun linked test cases and adjacent regression (especially E2E paths), close with evidence.

## 13. Risks & Mitigations
- AI provider latency/outage or drift: Impact High, Likelihood Medium; Mitigation: fallback provider, retries with backoff, mock provider for tests, latency monitoring with alerts.
- Queue backlog affecting 20s target: Impact High, Likelihood Medium; Mitigation: autoscale workers, alert on queue depth, prioritize optimize jobs, load-test concurrency.
- Signed URL or tenancy misconfiguration leaking data: Impact High, Likelihood Low; Mitigation: automated ownership tests, negative access tests, short TTLs, audit logs.
- Parsing accuracy below expectations: Impact Medium, Likelihood Medium; Mitigation: validation against sample set, re-run parse option, highlight detected sections for user confirmation.
- Ambiguous UX/error copy leading to user confusion: Impact Medium, Likelihood Medium; Mitigation: UI review against UX copy, consistency checks on banners/toasts, usability smoke.
- Limited accessibility coverage in MVP: Impact Medium, Likelihood Medium; Mitigation: basic A11y checklist, focus/contrast checks, log gaps for post-MVP.
- Payment/credit flag behavior divergence: Impact Medium, Likelihood Medium; Mitigation: scenarios with flag on/off, balance edge cases, ledger audits.

## 14. Out of Scope for MVP
- Heavy-load/stress testing beyond targeted concurrency; long-duration soak tests.
- Full penetration testing and formal security audits.
- Full WCAG compliance; only basic accessibility checks included.
- Exhaustive cross-browser/device matrix beyond latest Chrome/Edge/Safari and responsive layouts.
- Non-English optimization quality, cover letter generation, ATS scoring, LinkedIn import, native mobile apps, advanced analytics dashboards.

## 15. Sign-off Criteria
- All Blocker/Critical defects resolved; no open High-severity issues impacting core flows.
- All key user journeys validated end-to-end on staging with evidence; exports downloadable.
- Acceptance criteria for all MVP user stories met; traceability matrix updated.
- Regression suite (automated + targeted manual) executed with passing results; smoke tests green after last deploy.
- Observability/alerts active; no unexplained errors in logs/metrics for uploads, optimization, exports over defined burn-in window.
