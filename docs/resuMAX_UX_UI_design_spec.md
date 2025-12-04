# resuMAX UX/UI Design Specification

## 1. Product Overview
### Value statement
resuMAX turns any resume and job description into a tailored, ATS-friendly output in minutes through guided uploads, AI rewrites, and transparent previews.

### Problem being solved
Job seekers spend excessive time tailoring resumes, struggle to match keywords, and lack confidence in AI outputs. resuMAX provides a fast, auditable path to optimized resumes with clear change control and safe handling of personal data.

### Personas
1) Guided First-Timer: Needs handholding through upload, pairing, and acceptance; prioritizes clarity and reassurance.  
2) Speed-Oriented Power User: Comfortable with AI, wants apply-all changes, quick retries, and version control.  
3) Privacy-Conscious Professional: Wants assurances about data isolation, needs predictable formats for ATS, expects clear audit trails and easy deletions.

## 2. Alignment Notes
- 10-minute activation goal -> short stepper (Upload Resume > Add Job Description > Optimize > Download) with progress indicator and inline time expectations.
- ATS-friendly, truthful outputs -> diff-first preview, change highlights, and per-change accept toggles before export; default conservative tone.
- Parsing reliability and errors -> visible validation (file type/size), retry CTA, and "upload another file" affordance on the same screen.
- History and auditability -> dashboard list with statuses, timestamps, version badges, and per-version actions (preview, download, diff, delete).
- Privacy and trust -> inline privacy note on uploads, lock icons on storage actions, and explicit "only you can see this file" copy.
- Credits (if enabled) -> credit pill in top nav, gating optimization CTA when depleted, and billing history under Settings.
- Performance and latency targets -> loader with "typically under 20s" hint plus timeout-handling that offers retry or contact support.

## 3. Information Architecture
- Authentication
  - Sign up / Login
  - Email verification confirmation
  - Password reset
- First-use onboarding
  - Tooltip or checklist overlay guiding first upload and JD pairing
- Dashboard
  - Resume library (uploads, optimized versions, statuses, timestamps, score)
  - Quick actions (Upload resume, Add JD, New optimization)
  - Notifications/toasts tray
- Resume upload
  - Drag-and-drop area + file picker
  - Validation messaging and file rules
- Job description intake
  - Paste field and file upload (PDF/DOCX/text)
  - JD metadata capture (title, company, location) and sanitation note
- Optimization workspace
  - Pairing selector (choose resume + JD)
  - Optimization request stepper and status
  - Diff/preview (side-by-side and unified views)
  - Accept-all / per-change controls, summary panel
- Exports and history
  - Download options (PDF, DOCX, Copy text)
  - Saved outputs list with version naming
- Settings
  - Profile (name, email, default job preferences)
  - Security (password reset trigger)
  - Billing (credits/subscription, receipts, refunds when enabled)
- Help and support
  - FAQ links, contact support, latency notice

## 4. User Clickthrough Flows
### Onboarding
1) Landing on empty dashboard shows hero card with "Start with your resume" CTA plus privacy reassurance.  
2) Tooltip checklist (0/3) pins to top-right: Upload resume > Add job description > Optimize and download.  
3) Dismissible helper modals include short video/gif optional; progress persists across sessions.  
Error branch: If user closes checklist, surface a subtle "Need guidance?" pill to reopen; if email not verified, block uploads with banner and "Resend link" CTA.

### Resume upload
1) User opens Upload Resume. Drag-and-drop/picker accepts PDF/DOCX, shows size limit and privacy note.  
2) File selected -> immediate client validation (type/size); failing validation shows inline red message and keeps CTA disabled.  
3) On upload start, show uploading state with filename, percentage, and cancel link.  
4) On parse success, display detected sections summary (Contact, Experience, Education, Skills) with "Looks good / Re-run parse" micro CTA.  
Error branch: Parse failure shows error banner ("We could not read this file") with retry and "Try a different format" links; keep the file card visible for reattempt.

### Job description upload
1) From dashboard or pairing prompt, user selects "Add job description."  
2) Paste field and optional file upload (PDF/DOCX/text) with 10 MB limit; sanitization note appears under field.  
3) Extracted title/company auto-fill; user can edit before saving.  
4) Saved JD appears in list; prompt to pair with a resume.  
Error branch: If metadata missing, prompt "Add a title so we can label your output"; if upload fails, preserve pasted text so user does not lose it.

### Resume optimization output
1) User selects resume + JD -> clicks "Optimize." Status chip shows queued -> processing -> generating.  
2) Summary panel loads first (keywords added, gaps, tone); diff view highlights additions/deletions by section.  
3) User can apply-all or toggle per change; a sticky footer shows "Save version & continue."  
4) After save, user previews final layout; can download (PDF/DOCX) or copy text; version appears in history with timestamp and score.  
Error branches: If generation exceeds time budget, show "Still working... <5s more" then fallback CTA "Email me when ready" while keeping place. If AI flags uncertain content, surface inline warning and keep original text selected by default. If credit balance empty (when enabled), gate "Optimize" with modal linking to Billing.

## 5. Low-Fidelity Wireframe Descriptions
### Login / Signup
- Centered card on light background; brand wordmark top-left of card; tabs for Login/Signup.  
- Inputs stacked; password rules hint below password field.  
- Primary CTA full width; secondary "Continue as guest" hidden (not in scope).  
- Footer links: Privacy, Terms, Support.

### Dashboard
- Top nav with logo, credit badge, help icon, profile menu (settings, logout).  
- Left column list of resumes with search/filter and status badges; right main panel shows selected item details.  
- Empty state card centered when no uploads, with CTA "Upload resume."  
- Secondary cards for "Recent optimizations" and "Tips to improve ATS fit."

### Resume Upload
- Two-column layout: left side explains supported formats and privacy; right side large dropzone with dashed border and upload icon.  
- Below dropzone: recent uploads list with status chips and delete/rename overflow menu.  
- Inline validation under dropzone; progress bar overlays dropzone during upload.

### JD Upload
- Similar two-column layout: left side shows "How we use your JD" with sanitization note; right side has paste area + "Upload file" button.  
- Metadata fields (title, company, location) appear under paste box.  
- Save CTA in sticky footer; "Pair with resume" selector appears after save.

### Optimization Preview
- Header with paired resume/JD dropdowns and score badge.  
- Body split view: left original, right optimized; toggle for unified view.  
- Change summary strip across top; per-section accordions with accept/reject toggles.  
- Sticky footer: "Apply all changes," "Save version," "Download."

### Download / Saved Results
- Grid or list of versions with timestamps, file type icons, and status labels.  
- Each card actions: Preview, Download (PDF/DOCX), Copy text, Delete.  
- Right sidebar shows selected version preview with highlights and audit trail (who/when applied changes).

## 6. UI Component Library (BRD-driven)
### File uploader
- Purpose: Accept resumes (PDF/DOCX <= 5 MB) and JDs (PDF/DOCX/text <= 10 MB) via drag-drop or picker.  
- States: default (dashed border, icon), hover (accent border + subtle shadow), uploading (progress + cancel), success (green check + file name), error (red text with rule reminder).  
- Behavior: Blocks unsupported types; preserves last file on failure for retry; displays privacy tooltip on hover.

### CTA buttons
- Primary: solid accent fill; Secondary: outlined; Tertiary: text link.  
- States: default, hover (elevated shade), focus (2px focus ring), loading (spinner replaces text), disabled (reduced opacity).  
- Behavior: Primary drives conversions (optimize, upload); prevent double-submit during loading.

### Modal dialogs
- Purpose: confirmations (delete, apply-all), credit gate, privacy reassurance.  
- States: default, warning (amber icon), success (green icon), error (red icon).  
- Behavior: dimmed backdrop; Escape/close icon; primary CTA right-aligned; destructive actions use danger styling; trap focus for accessibility.

### Cards
- Purpose: display resumes, JDs, and saved versions with status and actions.  
- States: default, hover (shadow + accent border), selected (accent left rail), error (red badge).  
- Behavior: Click opens details; overflow menu for rename/delete; badges for status (pending, in progress, completed, failed).

### Progress indicator
- Purpose: communicate pipeline states (queued, parsing, optimizing, ready).  
- States: segmented stepper for long flows; inline spinner for short waits; error state offers retry.  
- Behavior: Shows time hint ("<20s typical"); updates in real time; persists in sticky header/footer.

### Toast notifications
- Purpose: transient feedback for uploads, saves, downloads, and errors.  
- States: info (blue), success (green), warning (amber), error (red).  
- Behavior: Auto-dismiss after 6s; pause on hover; include "View details" link for errors.

## 7. Visual Style Guide
- Typography: Headings - "Sora" (600/700); Body - "Work Sans" (400/500); Mono - "JetBrains Mono" for code-like diffs; sizes follow 8pt scale (12/14/16/20/24/32).  
- Color palette:  
  - Primary accent: Teal #12B8A6 for CTAs/links.  
  - Primary dark: Navy #0F172A for text/headings.  
  - Secondary: Sky #38BDF8 for info states.  
  - Success: #22C55E; Warning: #F59E0B; Error: #EF4444.  
  - Neutrals: #0B1220 (bg depth), #111827, #1F2937, #E5E7EB, #F8FAFC for surfaces and borders.  
- Spacing and grid: 8pt base spacing; cards 16-24pt padding; layout grid 12 columns with 24px gutters desktop, 4 columns mobile; components align to 4px baseline.  
- Iconography: Rounded-corner linear icons, 2px stroke, consistent with accent color; avoid aggressive fills; use lock/shield icons sparingly for trust cues.

## 8. UX Copywriting Examples (encouraging, professional, confidence-building)
- Empty states: "No resumes yet. Drop a PDF or DOCX to get your first optimization in under 2 minutes."  
- Onboarding tooltip: "Three quick steps: upload your resume, add a job description, preview changes. We'll guide you."  
- Confirmation: "Optimization saved and ready. Download now or reuse this version anytime."  
- Progress: "Optimizing now - most results arrive in under 20 seconds. You can navigate elsewhere and we'll notify you."  
- AI explanation: "These suggestions are grounded in your original resume and the job description. Keep only what feels accurate - your original text stays safe."

## 9. Prototyping Notes for Figma
- Link hotspots on primary CTAs (Upload, Optimize, Save version, Download) and on cards in the dashboard and history list.  
- Hover states: buttons lighten by 4-6% with focus ring; cards gain subtle shadow; dropzones thicken border and change icon tint.  
- Modals: use overlay with 12px corner radius; animate in with 150ms ease-out; disable background scroll; ESC and close icon both dismiss.  
- Screen transitions: fade/slide between dashboard and upload/optimization screens; stepper advances animate with progress bar fill.  
- Diff interactions: toggle switch between side-by-side and unified views; per-change accept toggles animate to confirm; sticky footer buttons always clickable.  
- Mobile guidance: collapsible accordions for sections, single-column layouts, bottom sheet for actions instead of sticky footer.
