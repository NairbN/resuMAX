from typing import Optional

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.config import settings
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    SignupRequest,
    VerifyRequest,
    ResendRequest,
)
from app.services import auth as auth_service
from app.core.security import csrf
from app.core.security import deps
from app.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])


def _set_cookies(response: Response, access: str, refresh: str):
    common = {
        "httponly": True,
        "secure": settings.cookie_secure,
        "samesite": settings.cookie_samesite,
        "domain": settings.cookie_domain,
    }
    response.set_cookie(
        "access_token",
        access,
        max_age=int(settings.access_expires.total_seconds()),
        **common,
    )
    response.set_cookie(
        "refresh_token",
        refresh,
        max_age=int(settings.refresh_expires.total_seconds()),
        **common,
    )
    # Set CSRF token for double-submit
    csrf_token = csrf.generate_csrf_token()
    response.set_cookie(
        csrf.CSRF_COOKIE,
        csrf_token,
        max_age=int(settings.refresh_expires.total_seconds()),
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
    )
    response.headers[csrf.CSRF_HEADER] = csrf_token


@router.get("/me", response_model=AuthResponse)
def me(current_user=Depends(deps.require_user)):
    return AuthResponse(user=current_user, needsVerification=not current_user.verified)


@router.post("/signup", response_model=AuthResponse, dependencies=[Depends(csrf.csrf_protect)])
def signup(payload: SignupRequest, response: Response, db: Session = Depends(get_db)):
    user, access, refresh, needs_verification = auth_service.signup(
        db, payload.email, payload.password
    )
    _set_cookies(response, access, refresh)
    return AuthResponse(token=access, user=user, needsVerification=needs_verification)


@router.post("/login", response_model=AuthResponse, dependencies=[Depends(csrf.csrf_protect)])
def login(payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user, access, refresh, needs_verification = auth_service.login(
        db, payload.email, payload.password
    )
    _set_cookies(response, access, refresh)
    return AuthResponse(token=access, user=user, needsVerification=needs_verification)


@router.post("/refresh", response_model=AuthResponse, dependencies=[Depends(csrf.csrf_protect)])
def refresh(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: Optional[str] = Cookie(default=None),
):
    user, access, new_refresh, needs_verification = auth_service.refresh_token(db, refresh_token)
    _set_cookies(response, access, new_refresh)
    return AuthResponse(token=access, user=user, needsVerification=needs_verification)


@router.post("/verify-email", response_model=AuthResponse, dependencies=[Depends(csrf.csrf_protect)])
def verify_email(payload: VerifyRequest, response: Response, db: Session = Depends(get_db)):
    user, access, refresh, needs_verification = auth_service.verify_email(db, payload.token)
    _set_cookies(response, access, refresh)
    return AuthResponse(token=access, user=user, needsVerification=needs_verification)


@router.post("/resend-verification", dependencies=[Depends(csrf.csrf_protect)])
def resend_verification(payload: ResendRequest, response: Response, db: Session = Depends(get_db)):
    result = auth_service.resend_verification(db, payload.email)
    # Refresh CSRF token on resend
    csrf_token = csrf.generate_csrf_token()
    response.set_cookie(
        csrf.CSRF_COOKIE,
        csrf_token,
        max_age=int(settings.refresh_expires.total_seconds()),
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        domain=settings.cookie_domain,
    )
    response.headers[csrf.CSRF_HEADER] = csrf_token
    return result


@router.post("/logout", dependencies=[Depends(csrf.csrf_protect)])
def logout(
    response: Response,
    db: Session = Depends(get_db),
    refresh_token: Optional[str] = Cookie(default=None),
):
    auth_service.logout(db, refresh_token)
    response.delete_cookie("access_token", domain=settings.cookie_domain)
    response.delete_cookie("refresh_token", domain=settings.cookie_domain)
    response.delete_cookie(csrf.CSRF_COOKIE, domain=settings.cookie_domain)
    return {"status": "logged_out"}
