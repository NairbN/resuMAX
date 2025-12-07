import datetime as dt
import time
import uuid
from typing import Dict, Optional, Tuple

import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.clients.redis import get_redis
from app.config import settings
from app.core.security.jwt import JwtError, decode_jwt, encode_jwt
from app.models import RefreshToken, User, VerificationToken
from app.schemas.auth import AuthUser


def _hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def _verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False


def _to_auth_user(user: User) -> AuthUser:
    return AuthUser(id=user.id, email=user.email, verified=user.verified)


class RateLimiter:
    def __init__(self, window_seconds: int, max_attempts: int):
        self.window = window_seconds
        self.max_attempts = max_attempts
        self.client = get_redis()
        self._fallback: Dict[str, list[float]] = {}

    def is_limited(self, key: str) -> bool:
        now = time.time()
        cutoff = now - self.window
        if self.client:
            try:
                pipe = self.client.pipeline()
                pipe.zremrangebyscore(key, 0, cutoff)
                pipe.zadd(key, {now: now})
                pipe.zcard(key)
                pipe.expire(key, int(self.window))
                _, _, count, _ = pipe.execute()
                return count >= self.max_attempts
            except Exception:
                self.client = None
        attempts = [t for t in self._fallback.get(key, []) if now - t < self.window]
        self._fallback[key] = attempts
        return len(attempts) >= self.max_attempts

    def record_failure(self, key: str):
        now = time.time()
        cutoff = now - self.window
        if self.client:
            try:
                pipe = self.client.pipeline()
                pipe.zremrangebyscore(key, 0, cutoff)
                pipe.zadd(key, {now: now})
                pipe.expire(key, int(self.window))
                pipe.execute()
                return
            except Exception:
                self.client = None
        else:
            self._fallback.setdefault(key, []).append(now)

    def clear(self, key: str):
        if self.client:
            try:
                self.client.delete(key)
                return
            except Exception:
                self.client = None
        else:
            self._fallback[key] = []


_rate_limiter = RateLimiter(settings.rate_limit_window_seconds, settings.rate_limit_attempts)


def _issue_tokens(db: Session, user: User) -> Tuple[str, str]:
    access = encode_jwt(
        {"sub": user.id, "email": user.email, "type": "access", "jti": str(uuid.uuid4())},
        int(settings.access_expires.total_seconds()),
    )
    refresh = encode_jwt(
        {"sub": user.id, "email": user.email, "type": "refresh", "jti": str(uuid.uuid4())},
        int(settings.refresh_expires.total_seconds()),
    )
    # revoke old refresh tokens and store the new one
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user.id, RefreshToken.revoked.is_(False)
    ).update({"revoked": True})
    db.add(
        RefreshToken(
            token=refresh,
            user_id=user.id,
            expires_at=dt.datetime.now(dt.timezone.utc) + settings.refresh_expires,
            revoked=False,
        )
    )
    db.commit()
    return access, refresh


def signup(db: Session, email: str, password: str):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    user = User(email=email, password_hash=_hash_password(password), verified=settings.auto_verify)
    db.add(user)
    db.commit()
    db.refresh(user)

    needs_verification = not user.verified
    if needs_verification:
        token = str(uuid.uuid4())
        db.add(
            VerificationToken(
                token=token,
                user_id=user.id,
                expires_at=dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=24),
                used=False,
            )
        )
        db.commit()
    access, refresh = _issue_tokens(db, user)
    return _to_auth_user(user), access, refresh, needs_verification


def login(db: Session, email: str, password: str):
    if _rate_limiter.is_limited(email):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many attempts"
        )
    user = db.query(User).filter(User.email == email).first()
    if not user:
        _rate_limiter.record_failure(email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    if not _verify_password(password, user.password_hash):
        _rate_limiter.record_failure(email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    _rate_limiter.clear(email)
    access, refresh = _issue_tokens(db, user)
    return _to_auth_user(user), access, refresh, not user.verified


def refresh_token(db: Session, token: Optional[str]):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    stored = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == token, RefreshToken.revoked.is_(False))
        .first()
    )
    if not stored:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    now = dt.datetime.now(dt.timezone.utc)
    expires_at = stored.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=dt.timezone.utc)
    if expires_at <= now:
        stored.revoked = True
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token")

    try:
        payload = decode_jwt(token)
    except JwtError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    if payload.get("sub") != stored.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(User).filter(User.id == stored.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    stored.revoked = True
    db.commit()
    access, new_refresh = _issue_tokens(db, user)
    return _to_auth_user(user), access, new_refresh, not user.verified


def verify_email(db: Session, token: str):
    record = (
        db.query(VerificationToken)
        .filter(VerificationToken.token == token, VerificationToken.used.is_(False))
        .first()
    )
    now = dt.datetime.now(dt.timezone.utc)
    if not record or record.expires_at <= now:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    user = db.query(User).filter(User.id == record.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")
    user.verified = True
    record.used = True
    db.commit()
    access, refresh = _issue_tokens(db, user)
    return _to_auth_user(user), access, refresh, False


def resend_verification(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.verified:
        return {"status": "already_verified"}
    token = str(uuid.uuid4())
    db.add(
        VerificationToken(
            token=token,
            user_id=user.id,
            expires_at=dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=24),
            used=False,
        )
    )
    db.commit()
    return {"status": "resent", "token": token}


def clear_state(db: Session):
    db.query(RefreshToken).delete()
    db.query(VerificationToken).delete()
    db.query(User).delete()
    db.commit()


def get_user_by_id(db: Session, user_id: str) -> Optional[AuthUser]:
    user = db.query(User).filter(User.id == user_id).first()
    return _to_auth_user(user) if user else None


def logout(db: Session, refresh_token: Optional[str]):
    if refresh_token:
        record = db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()
        if record:
            record.revoked = True
            db.commit()
