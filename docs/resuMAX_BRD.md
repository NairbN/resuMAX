# resuMAX Business Requirements Document
Version 0.1 | 2025-12-03 | Author: Codex

## 1. Executive Summary
- Purpose: resuMAX helps job seekers align resumes to job postings using AI to rewrite and format.
- Problem: manual tailoring is time consuming and lacks data-driven alignment, causing ATS drop-offs.
- Core value: automated alignment, measurable ATS-friendly improvements, fast preview and export.

## 2. Business Objectives
- Acquire and activate job seekers by enabling them to optimize resumes in under 10 minutes.
- Improve interview invite rates by delivering resumes that match role keywords and structure.
- Establish recurring revenue through subscriptions or credit packs once value proven.
- Success metrics (MVP targets):
  - DAU: 500 daily active users within 90 days of launch.
  - Conversion: 10 percent of active users complete at least one optimization.
  - Paid conversion (if payments on): 5 percent of active users purchase credits or subscription.
  - Resume improvement accuracy: 80 percent of users rate suggested changes as relevant.
  - Flow completion: 80 percent of resume uploads proceed through optimization to download.
  - Latency: 90 percent of optimizations returned within 20 seconds.

## 3. Stakeholders and Actors
| Actor | Role | Goals or Responsibilities |
| --- | --- | --- |
| Job seekers | Primary end users uploading resumes and JDs | Get tailored, ATS friendly resumes quickly |
| Admins and support | Manage users, monitor errors, handle refunds or abuse | Keep platform healthy and compliant |
| AI model services | LLMs and NLP pipelines used for parsing and rewriting | Provide accurate, safe, traceable generations |
| Third party storage | Cloud object storage for resumes and exports | Durable, encrypted storage and retrieval |
| Payment processor | Handles billing, subscriptions, and refunds | Secure transactions and reporting |
| Observability tools | Logging and monitoring | Track latency, failures, and user funnels |

## 4. Scope
### 4.1 In scope for MVP
- Account creation and login.
- Resume upload, parsing, and section detection.
- Job description upload or paste.
- AI powered optimization suggestions and full rewrite aligned to JD.
- Preview, accept, and download optimized resume as PDF or DOCX.
- Basic dashboard with history of uploads and optimized versions.
- Optional credit based payment gate if enabled.
### 4.2 Out of scope for MVP
- Real time collaboration or commenting.
- Native mobile apps.
- Multi language generation beyond English.
- Direct ATS submissions or LinkedIn one click apply.
- Advanced analytics dashboards for recruiters.

## 5. Functional Requirements
### 5.1 Resume upload and parsing
- FR1: The system shall accept resume uploads in PDF and DOCX formats via drag and drop and file picker.
- FR2: The system shall enforce a maximum file size of 5 MB and display a validation error if exceeded.
- FR3: The system shall extract text and section structure from uploaded resumes with at least 90 percent section fidelity.
- FR4: The system shall detect and surface key entities such as contact information, education, work experience, skills, and dates.
- FR5: The system shall return a clear error message with retry guidance when parsing fails.

### 5.2 User dashboard
- FR6: The system shall display a list of each user's uploaded resumes and generated optimized versions with timestamps and status.
- FR7: The system shall show an optimization status badge per resume including states pending, in progress, completed, failed.
- FR8: The system shall show a comparison score indicating alignment between the resume and the paired job description.
- FR9: The system shall allow users to view past versions and open a side by side diff of original versus optimized text.
- FR10: The system shall allow users to rename or delete resumes and optimized outputs within their own account.

### 5.3 Job description upload
- FR11: The system shall allow users to paste or upload a job description in text, PDF, or DOCX up to 10 MB.
- FR12: The system shall sanitize and normalize pasted or uploaded job descriptions to remove headers, footers, and personal data.
- FR13: The system shall associate a job description with a selected resume for optimization.
- FR14: The system shall store job title, company, and location metadata when available for labeling results.

### 5.4 Resume optimization engine
- FR15: The system shall analyze differences between the resume and job description to extract missing keywords and competencies.
- FR16: The system shall generate rewritten bullet points and sections aligned to the job description while preserving truthfulness of claims.
- FR17: The system shall provide an overall optimization summary that highlights key changes, gaps, and suggested skill emphasis.
- FR18: The system shall allow users to apply suggested changes individually or apply all changes at once before export.
- FR19: The system shall log generated changes and user acceptance choices for auditability and rollback.

### 5.5 Download and export flows
- FR20: The system shall present a preview of the optimized resume with change highlights before download.
- FR21: The system shall allow export to PDF and DOCX while maintaining layout and preserving contact information.
- FR22: The system shall provide a copy to clipboard option for plain text export of the optimized resume.
- FR23: The system shall store and label downloaded versions so users can re download prior outputs.

### 5.6 User account management
- FR24: The system shall support account creation, login, and logout via email and password.
- FR25: The system shall support password reset via email verification and enforce strong password rules.
- FR26: The system shall allow users to update profile fields including name, contact email, and default job preferences.
- FR27: The system shall enforce account level data isolation so users only see their own resumes and outputs.

### 5.7 Payment and credits (if enabled)
- FR28: The system shall allow users to purchase optimization credits or subscribe via a payment processor such as Stripe.
- FR29: The system shall display remaining credits or subscription status and deduct credits when an optimization is initiated.
- FR30: The system shall provide a billing history view with receipts and refund indicators.

## 6. Non functional requirements
- NF1: Scalability: The system shall support at least 10,000 users storing up to 20 optimized resumes each without performance degradation.
- NF2: Performance: The system shall return optimization results within 20 seconds for 90 percent of requests and within 30 seconds for 99 percent.
- NF3: Availability: The system shall maintain 99.5 percent uptime monthly for user facing flows.
- NF4: Security: The system shall encrypt data in transit with TLS 1.2 or higher and at rest using provider managed encryption.
- NF5: Privacy: The system shall isolate customer data per account and prevent cross tenant access via authorization checks on every request.
- NF6: Compliance readiness: The system shall support data deletion upon user request and log access to personal data for auditability.
- NF7: Reliability: The system shall queue optimization requests and retry failed AI calls up to two times before marking failed.
- NF8: Observability: The system shall capture structured logs, latency metrics, and error rates for uploads, parsing, optimization, and exports.

## 7. User stories
1. As a job seeker, I want to upload my resume so that I can get tailored recommendations for a specific job.
2. As a job seeker, I want to paste a job description so that the system can align my resume to it.
3. As a job seeker, I want to see missing keywords so that I can decide whether to accept suggestions.
4. As a job seeker, I want to preview the optimized resume with highlights so that I can trust what changed.
5. As a job seeker, I want to download the optimized resume as PDF so that I can submit it to applications.
6. As a job seeker, I want to copy the optimized text so that I can update my existing resume template.
7. As a job seeker, I want to save multiple optimized versions so that I can reuse them for similar roles.
8. As a returning user, I want to view my history so that I can quickly re download past outputs.
9. As a cautious user, I want reassurance that my resume is private so that I feel safe uploading it.
10. As a power user, I want to apply all suggested changes in one click so that I can move quickly.
11. As a new user, I want onboarding guidance so that I can complete my first optimization without friction.
12. As a paid user, I want to see my remaining credits so that I know how many optimizations I can run.
13. As an admin, I want to monitor failed optimizations so that I can resolve issues proactively.
14. As an admin, I want to refund credits when appropriate so that I can support users.
15. As a user, I want to reset my password so that I can regain access if I forget it.

## 8. End to end user journeys and flows
- Registration and activation: user visits sign up, enters email and password, verifies email link, lands on empty dashboard with guided tooltip to upload resume.
- Resume upload and parsing: user drags PDF, system validates size and format, uploads to storage, triggers parsing pipeline, displays parsed sections and any issues.
- Job description upload: user pastes JD text or uploads file, system cleans formatting, extracts title and company, confirms pairing with a selected resume.
- Optimization preview and acceptance: user starts optimization, system queues request, AI generates summary and rewritten sections, UI shows diff with accept all or per change toggles, user accepts, version saved.
- Export and download: after acceptance, user previews final layout, downloads as PDF or DOCX, system stores version record and decrements credits if enabled.
- Return visit using history: user logs in, dashboard shows prior optimizations, user re downloads or re runs optimization against a new JD reusing stored resume.

## 9. Assumptions and dependencies
- Users provide resumes in common formats (PDF, DOCX) and in English.
- AI models are reachable and deliver reasonably accurate, deterministic results with prompt engineering and safety filters.
- Cloud object storage is available for encrypted storage of uploaded and generated files.
- Email service is available for verification and password reset.
- Payment processing and compliance depend on third party providers when enabled.
- Browser access is modern (latest Chrome, Edge, Safari) with JavaScript enabled.

## 10. Risks
- Model hallucination may introduce inaccurate claims; mitigation includes grounding on extracted resume facts and user confirmation.
- Resume plagiarism concerns if AI suggests content from training data; mitigation includes originality checks and disclaimers.
- Incorrect suggestions or formatting errors could harm user chances; mitigation includes diff preview, opt in controls, and QA tests.
- Data leakage risk through logs or mis scoped access; mitigation includes strict PII scrubbing and access controls.
- Payment disputes or failed charges could affect trust; mitigation includes clear receipts and support playbooks.

## 11. Acceptance criteria for MVP
- At least 80 percent of users who upload a resume and JD receive an optimized preview within 30 seconds.
- At least 80 percent of users successfully download an optimized resume in PDF or DOCX.
- At least 90 percent of uploads within supported formats and size limits complete parsing without manual intervention.
- Basic authentication flows (sign up, login, logout, password reset) function with email verification.
- If payments are enabled, users can purchase credits and see accurate balances and deductions.
- Privacy controls enforced so that no user can access another user's resumes or outputs, validated by automated tests.
- Observability dashboards show upload, optimization, and download success and latency metrics.

## 12. Future enhancements (post MVP)
- ATS compatibility scoring and report cards by role or company.
- Tailored cover letter generation linked to the same job description.
- LinkedIn profile import and parsing to seed resume content.
- Interview question generation based on job description and resume gaps.
- Career coaching conversational agent for ongoing guidance.
- Resume gap filler suggestions and achievement quantification helpers.
- Multi language support and localization of outputs.
- Collaboration with mentors or career coaches with controlled sharing links.
- Browser extension to scrape job descriptions directly from job boards.
- Analytics for users showing performance trends and keyword coverage across roles.
