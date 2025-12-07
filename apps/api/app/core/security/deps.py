from typing import Optional

from fastapi import Cookie, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security.jwt import JwtError, decode_jwt
from app.db.session import get_db
from app.services import auth as auth_service


def _get_token_from_request(
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
    access_cookie: Optional[str] = Cookie(default=None, alias="access_token"),
) -> Optional[str]:
    if authorization and authorization.startswith("Bearer "):
        return authorization.split(" ", 1)[1]
    return access_cookie


def require_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(_get_token_from_request),
):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    try:
        payload = decode_jwt(token)
    except JwtError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))

    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")

    user = auth_service.get_user_by_id(db, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def require_verified_user(user=Depends(require_user)):
    if not user.verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified",
        )
    return user
