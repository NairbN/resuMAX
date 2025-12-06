Auth frontend expectations for backend

- Endpoints expected
  - POST /auth/signup → { user, needsVerification?, token? }, sets httpOnly access/refresh cookies.
  - POST /auth/login → same shape, sets cookies.
  - POST /auth/logout → clears/revokes cookies.
  - POST /auth/resend-verification
  - POST /auth/verify-email (body { token })
  - GET /auth/me → { user, needsVerification? }
  - POST /auth/refresh → sets refreshed cookies.

- Auth/storage
  - Cookie-based session: httpOnly cookies for access/refresh, client uses withCredentials: true.
  - CSRF: client sends X-CSRF-Token on non-GET; backend should set a CSRF cookie (expected name XSRF-TOKEN) and validate it.

- Responses/flags
  - Include needsVerification: true for unverified accounts; UI blocks uploads/CTAs until false.
  - Errors: 401 → invalid creds; 429 → rate limit message. Validation errors can be { detail: "..." } or { detail: [ { msg } ] }.

- Lifecycle
  - Client calls me on load and refresh every ~10 minutes; on refresh failure, it logs out. Implement refresh accordingly.

- Navigation
  - On successful login/signup, client routes to /dashboard and expects the session to be valid there.

- Config
  - Mock toggle: NEXT_PUBLIC_USE_AUTH_MOCK=true skips backend; default uses real API.
  - Adjust CSRF cookie/header names in src/services/api/client.ts if backend uses different names.
