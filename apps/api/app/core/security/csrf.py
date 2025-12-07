import secrets
from fastapi import Cookie, Header, HTTPException, status

CSRF_HEADER = "X-CSRF-Token"
CSRF_COOKIE = "XSRF-TOKEN"


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def csrf_protect(
    csrf_header: str | None = Header(default=None, alias=CSRF_HEADER),
    csrf_cookie: str | None = Cookie(default=None, alias=CSRF_COOKIE),
):
    """
    Simple double-submit CSRF check. If a CSRF cookie is present, the header must match.
    If no cookie is present (first request), no enforcement is applied.
    """
    if csrf_cookie and csrf_header != csrf_cookie:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF token mismatch",
        )
    return csrf_cookie
