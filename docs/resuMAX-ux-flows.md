# resuMAX — UX Flow Document

## 1. Product Overview
- resuMAX helps job seekers align resumes to target job descriptions using AI-driven rewrites, diff previews, and exports (PDF, DOCX, text) in under 10 minutes.
- Designed for guided first-timers and speed-oriented users needing ATS-friendly, truthful outputs with privacy and auditability.
- Provides dashboard/history to manage resumes, JDs, optimizations, and credits (when enabled) with status tracking.

## 2. Personas
- Guided First-Timer: Goals: finish first upload/JD pairing and trust the AI; Frustrations: unclear steps, fear of losing progress, skepticism; Needs: checklist onboarding, visible validation, privacy reassurance, undo/accept controls.
- Speed-Oriented Power User: Goals: rapid uploads, apply-all changes, quick retries, version control; Frustrations: slow states, redundant inputs, hidden status or credit gating; Needs: keyboard-friendly actions, sticky footers, live status chips, retry/resume without re-upload.
- Privacy-Conscious Professional: Goals: keep data isolated, preserve truthful content, maintain ATS-safe format; Frustrations: unclear storage, unexpected tone changes; Needs: inline privacy copy, conservative defaults, clear delete/rename, audit trail of versions.

## 3. Information Architecture
- Authentication
  - Login / Signup
  - Email verification confirmation
  - Password reset
- Onboarding
  - Dashboard empty state hero with "Start with your resume"
  - Tooltip checklist (Upload resume > Add JD > Optimize > Download)
- Dashboard
  - Resume library list with statuses, timestamps, score, search/filter
  - JD list or pairing prompt
  - Quick actions: Upload resume, Add JD, New optimization
  - Notifications/toasts tray; latency notice
- Resume Upload
  - Drag-drop/picker card with rules and privacy note
  - Validation messaging, progress, cancel
  - Recent uploads with status chips and overflow menu (rename/delete)
- Job Description Intake
  - Paste area + file upload (PDF/DOCX/text)
  - Metadata fields (title, company, location) and sanitization note
- Pairing & Optimization Workspace
  - Resume + JD selectors
  - Stepper/status chips (queued > processing > generating > ready)
  - Summary panel, diff/preview (side-by-side/unified)
  - Accept-all/per-change toggles; sticky footer actions
- Exports & History
  - Saved versions grid/list with timestamps, score, status
  - Actions: Preview, Download PDF/DOCX, Copy text, Delete
- Settings
  - Profile (name, email, preferences)
  - Security (password reset trigger)
  - Billing (credits/subscription, receipts/refunds when enabled)
- Help & Support
  - FAQ links, contact support, privacy/latency notices

## 4. Core User Flows
### Flow: Onboarding / Login
Goal: Authenticate and guide users to first upload with verification handled.
Primary Path:
1. User opens app; sees login/signup card.
2. Enter email/password; submit; if new, verification email sent.
3. After verified, land on dashboard empty state with hero CTA and checklist (0/3).
4. Checklist highlights "Upload resume" then "Add job description" then "Optimize & download."
Outcome: Authenticated user in guided dashboard, ready to upload.
Alternate Paths:
- If email not verified, block uploads with banner and "Resend link" CTA.
- If forgot password, trigger reset; return to login after success.
- If returning user, bypass checklist focus and show history with ability to reopen guidance pill.

### Flow: Resume Upload
Goal: Capture resume file, parse sections, and store in library for pairing.
Primary Path:
1. From dashboard, click "Upload resume" or checklist item.
2. Drag/drop or pick PDF/DOCX; client validates type and <=5 MB; rules shown inline.
3. On submit, show uploading progress with filename and cancel link.
4. After upload, parsing runs; show detected sections summary with "Looks good / Re-run parse."
5. Save resume to library with status chip (completed) and timestamp; resume selectable for optimization.
Outcome: Parsed resume stored with status and visible in library.
Alternate Paths:
- If unsupported type/size, show inline error, keep file card for retry.
- If parsing fails, show error banner ("We could not read this file") with retry and "Try a different format" links; preserve file reference.
- If user cancels upload, return to dropzone with prior checklist state.

### Flow: Job Description Upload
Goal: Capture JD content and metadata to pair with a resume.
Primary Path:
1. From dashboard or prompt, select "Add job description."
2. Paste text or upload PDF/DOCX/text (<=10 MB); sanitization note visible.
3. System extracts title/company/location; user can edit before saving.
4. Save JD; show in list with label and prompt to pair with a resume.
Outcome: JD saved with metadata and ready for pairing.
Alternate Paths:
- If JD empty or missing title, prompt "Add a title so we can label your output" and block save.
- If upload fails, preserve pasted text and keep modal open with retry CTA.
- If user dismisses, keep unsaved text until explicit cancel confirmation.

### Flow: AI Optimization / Result Review
Goal: Generate and review AI-optimized resume aligned to JD.
Primary Path:
1. User selects resume + JD; confirm pairing.
2. If credits enabled, check balance; if sufficient, click "Optimize" (primary CTA).
3. Status chip shows queued > processing > generating with "<20s typical" hint.
4. Summary panel loads first (keywords added, gaps, tone); diff view highlights additions/deletions by section.
5. User applies all or toggles per change; sticky footer shows "Save version & continue."
6. Save accepted changes as new version; update history with status and score.
Outcome: Optimized version saved with accepted changes ready for preview/export; credits deducted if applicable.
Alternate Paths:
- If AI exceeds time budget, show "Still working... <5s more" then fallback "Email me when ready" while keeping screen state.
- If AI flags uncertain content, show inline warning and keep original text selected by default.
- If credit balance empty, show modal gating optimization with link to Billing.
- If generation fails, show error toast/banner with retry and contact support link; preserve previous selection.

### Flow: Saving / Downloading Output
Goal: Confirm optimized layout and export or reuse versions.
Primary Path:
1. After saving changes, user opens preview; layout shows highlights.
2. Choose export: Download PDF, Download DOCX, or Copy text; CTA in sticky footer/sidebar.
3. System generates file, triggers download, and stores version record with timestamp and status.
4. Version appears in history grid/list; user can rename, delete, or re-download.
Outcome: User obtains optimized resume file and history updated for future reuse.
Alternate Paths:
- If export fails, show toast with retry option and keep preview accessible.
- If user navigates away mid-export, background job continues and toast appears when ready.
- If deletion requested, show confirmation modal; on confirm, remove version but keep original resume.

## 5. Screen Responsibility Mapping
### Screen: Login / Signup
Purpose: Authenticate users and enforce verification before access.
Entry points: Direct URL, deep links after logout, expired session redirect.
Exit points: Verified users to dashboard; unverified flows to verification banner.
Primary actions: Login, create account, resend verification email, start password reset.
Required UI elements: Tabs for login/signup, email/password inputs, password rules hint, primary CTA, verification status banner, links to Privacy/Terms/Support.
Validation rules: Email format required; password complexity; block submit while invalid; throttle repeated failed attempts.
System interactions: Auth API calls, send verification email, set session tokens, display auth error codes.

### Screen: Dashboard
Purpose: Home for uploads, pairing, history, and quick actions.
Entry points: Post-login, return visits, navigation from settings/help.
Exit points: Resume upload, JD upload, optimization workspace, settings/billing, logout.
Primary actions: Upload resume, Add JD, start New optimization, open history item, rename/delete records.
Required UI elements: Top nav (logo, credit badge, help icon, profile menu), resume/JD lists with status chips and score, search/filter, empty-state hero, checklist pill, notifications/toasts.
Validation rules: Prevent actions if email unverified or no resume selected; disable Optimize if pairing incomplete or credits depleted.
System interactions: Fetch libraries and statuses, poll optimization states, fetch credit balance, log user actions for analytics.

### Screen: Resume Upload
Purpose: Collect resume file and parse content.
Entry points: Dashboard CTA or checklist; re-upload from error state.
Exit points: Back to dashboard with new resume; parsing error path; cancel to dashboard.
Primary actions: Select/drag file, submit upload, cancel upload, accept parsed summary, re-run parse.
Required UI elements: Dropzone/picker with rules (PDF/DOCX, <=5 MB), privacy note/lock icon, progress bar with cancel, parsed sections summary, inline error banner.
Validation rules: Client-side type/size checks; disable submit when invalid; block parsing if upload incomplete.
System interactions: Upload to storage, trigger parsing pipeline, receive parsed sections, log failures.

### Screen: Job Description Upload
Purpose: Capture JD content and metadata for pairing.
Entry points: Dashboard CTA, pairing prompt when JD missing, from optimization workspace.
Exit points: Back to dashboard with saved JD; error retry loop; cancel with unsaved content warning.
Primary actions: Paste or upload JD, edit title/company/location, save, pair with resume.
Required UI elements: Paste area, file upload button, sanitization note, metadata fields, sticky footer Save, inline errors.
Validation rules: Required text/title before save; enforce <=10 MB on uploads; preserve pasted text on errors.
System interactions: Upload/sanitize JD, extract metadata, persist JD record, confirm pairing.

### Screen: Optimization Workspace / Preview
Purpose: Run AI optimization, review diffs, and save accepted changes.
Entry points: From dashboard selecting resume + JD, from history re-run with new JD.
Exit points: Save version then go to preview/export; navigate back to dashboard; retry on error.
Primary actions: Choose resume/JD, start Optimize, toggle side-by-side/unified view, accept/reject changes, apply all, save version.
Required UI elements: Pairing selectors, status chips/stepper, summary panel, diff view, per-change toggles, warning indicators, sticky footer ("Apply all", "Save version", "Download").
Validation rules: Require valid resume + JD selection; enforce credit check (if enabled); disable CTAs during processing; guard against unsaved changes when navigating away.
System interactions: Queue optimization request, stream status updates, log acceptance choices, store version, decrement credits, handle retries/timeouts.

### Screen: Download & History
Purpose: Provide access to saved versions and exports.
Entry points: From workspace after save, dashboard history card, toast "View details."
Exit points: Back to dashboard; open preview; start new optimization using existing resume/JD.
Primary actions: Preview version, download PDF/DOCX, copy text, rename, delete, re-run optimization.
Required UI elements: Grid/list of versions with timestamps/status/score, action buttons, preview pane with highlights, audit trail notes.
Validation rules: Prevent download if generation incomplete/failed; confirm destructive deletes; maintain unique names or allow rename with inline validation.
System interactions: Fetch version metadata/files, trigger export jobs, log downloads, handle delete requests with storage cleanup.

### Screen: Settings / Billing (if enabled)
Purpose: Manage profile, security, and credit/subscription state.
Entry points: Profile menu, credit gate modal link, onboarding prompts for verification.
Exit points: Back to dashboard; payment processor flows; logout.
Primary actions: Update profile, trigger password reset, view receipts, purchase credits/subscription, request refund (admin support).
Required UI elements: Profile form fields, password reset trigger, credit balance pill, billing history list, payment CTAs, refund indicators.
Validation rules: Required name/email formatting; block billing actions if processor unavailable; display read-only states when not enabled.
System interactions: Update user profile, call payment processor, fetch receipts, adjust credit balances, log billing events.

## 6. Behavioral / Interaction Logic
- Validation: Enforce file types and size limits (resume PDF/DOCX <=5 MB; JD text/PDF/DOCX <=10 MB); require email verification before uploads; require title for JD labeling; ensure resume + JD selected before Optimize; enforce password strength on auth.
- Error handling: Inline errors near fields; keep uploaded/pasted content available for retry; show parse failure banner with retry/different format links; display credit/verification gates as blocking modals or banners; AI uncertainty flagged with warning and default to original text.
- Loading states: Uploads show filename, percentage, and cancel; optimization uses status chips/stepper with "<20s typical"; diff/summary loads progressively with spinners; exports show spinner and toast on completion.
- Confirmation: After save/export show success toast ("Optimization saved and ready"); destructive actions (delete, apply-all) require modal confirmation; email verification prompts with "Resend link."
- Retry: Upload/parse failures provide retry CTA; optimization failures allow re-run with preserved selections; timeouts offer "Email me when ready" or manual retry; password reset available after failed login attempts.
- Navigation rules: Block optimize/download until validations pass; preserve unsaved changes when navigating away (prompt confirmation); allow browsing dashboard while optimization runs with status updates and toasts; keep checklist progress across sessions.

## 7. Component Mapping
- Component: Buttons
  Used in: All primary flows (upload, optimize, save, download, billing).
  States: default, hover, focus (2px ring), loading (spinner replaces text), disabled.
  Behavior: Primary drives conversions; prevent double-submit while loading; destructive styled for delete.
- Component: Upload Tile
  Used in: Resume upload, JD upload.
  States: default dashed, hover accent, uploading with progress/cancel, success check, error with rule reminder.
  Behavior: Accepts drag/drop or picker; blocks unsupported types; preserves last file on failure; shows privacy tooltip on hover.
- Component: Resume/JD/Version Card
  Used in: Dashboard lists, history.
  States: default, hover with shadow, selected accent rail, error badge, status chips (pending, in progress, completed, failed).
  Behavior: Click opens details; overflow menu for rename/delete; shows timestamps, score, and actions (preview, download).
- Component: Modal
  Used in: Apply-all confirmation, delete confirmation, credit gate, privacy reassurance.
  States: default, warning, success, error with contextual icon.
  Behavior: Dimmed backdrop; Escape/close icon; primary CTA right-aligned; focus trapped; destructive uses danger styling.
- Component: Toast Notification
  Used in: Upload success/fail, optimization complete, export ready, errors.
  States: info, success, warning, error; auto-dismiss after ~6s; pause on hover.
  Behavior: Includes "View details" link for errors; stackable without overlap.
- Component: Progress Indicator
  Used in: Stepper for overall flow, inline for uploads/optimization/export.
  States: segmented stepper (Upload > JD > Optimize > Download), spinner for short waits, error state with retry.
  Behavior: Shows time hint; updates in real time; persists in sticky header/footer during processing.

## 8. Edge Case Scenarios
- Invalid file type or >5 MB resume (or >10 MB JD): show inline red message, disable submit, keep file tile for retry.
- Empty JD or missing title: block save; prompt to add minimal info; preserve pasted text.
- Parse failure: keep file card, show retry/different format links; allow re-run parse.
- AI optimization failure or timeout: show banner/toast with retry; offer "Email me when ready"; retain selections and prior version.
- Credit depleted (if enabled): disable Optimize, show modal linking to Billing; resume upload still allowed.
- Email not verified: block uploads with banner and resend CTA.
- Returning user: dashboard loads history with status badges; allow re-download or re-run without re-uploading; checklist reopenable via "Need guidance?" pill.
- Deletion of versions: confirmation required; original resumes remain intact.
- Network interruption during upload/export: show failure toast, allow retry without clearing previous inputs.

## 9. Design Flow Principles
- Keep primary CTA consistently placed (sticky footer for workspace/export; top-right for onboarding hero).
- Validate early and inline before navigation or processing; block next steps until required inputs set.
- Provide real-time feedback on progress with explicit time expectations and statuses.
- Preserve user input and context across errors, retries, and navigation; never discard uploads/paste by default.
- Default to truthful, conservative AI outputs with diffs and accept controls; warn on uncertain changes.
- Surface privacy and trust cues near uploads and storage actions; include clear delete/rename paths.
- Allow users to continue browsing while long-running tasks finish, with toasts and status chips for completion.
