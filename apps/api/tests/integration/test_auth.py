import pytest
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.services import auth as auth_service
from app.models import RefreshToken


def _csrf_header(client: TestClient):
    token = client.cookies.get("XSRF-TOKEN")
    return {"X-CSRF-Token": token} if token else {}


def test_signup_verify_refresh_with_csrf(db_session):
    client = TestClient(app)

    res = client.post("/auth/signup", json={"email": "a@test.com", "password": "password123"})
    assert res.status_code == 200
    body = res.json()
    if body["needsVerification"]:
        # simulate verification for non-auto-verify mode
        res = client.post(
            "/auth/resend-verification",
            json={"email": "a@test.com"},
            headers=_csrf_header(client),
        )
        token = res.json()["token"]
        res = client.post(
            "/auth/verify-email",
            json={"token": token},
            headers=_csrf_header(client),
        )
        assert res.status_code == 200
        body = res.json()
    assert body["needsVerification"] is False
    assert body["user"]["verified"] is True
    assert client.cookies.get("access_token")
    assert client.cookies.get("refresh_token")

    # Refresh with CSRF header should succeed
    res = client.post("/auth/refresh", headers=_csrf_header(client))
    assert res.status_code == 200
    assert res.json()["user"]["verified"] is True


def test_refresh_requires_csrf_header(db_session):
    client = TestClient(app)
    client.post("/auth/signup", json={"email": "b@test.com", "password": "password123"})

    # Missing header should be blocked because cookie exists
    res = client.post("/auth/refresh")
    assert res.status_code == 403

    old_refresh = client.cookies.get("refresh_token")
    old_csrf = client.cookies.get("XSRF-TOKEN")

    res = client.post("/auth/refresh", headers=_csrf_header(client))
    assert res.status_code == 200

    # old refresh should be invalidated after use
    with pytest.raises(HTTPException) as excinfo:
        auth_service.refresh_token(db_session, old_refresh)
    assert excinfo.value.status_code == 401


def test_login_rate_limits_after_failures(db_session):
    client = TestClient(app)
    client.post("/auth/signup", json={"email": "c@test.com", "password": "password123"})

    for _ in range(5):
        res = client.post(
            "/auth/login",
            json={"email": "c@test.com", "password": "wrongpass"},
            headers=_csrf_header(client),
        )
        assert res.status_code == 401

    res = client.post(
        "/auth/login",
        json={"email": "c@test.com", "password": "wrongpass"},
        headers=_csrf_header(client),
    )
    assert res.status_code == 429


def test_unknown_user_does_not_count_toward_rate_limit(db_session):
    client = TestClient(app)
    # Repeated invalid attempts for non-existent user should stay 401, not 429
    for _ in range(6):
        res = client.post(
            "/auth/login",
            json={"email": "unknown@test.com", "password": "wrongpass"},
            headers=_csrf_header(client),
        )
        assert res.status_code == 401

    # Now create a user and ensure rate limit applies only to the real user
    client.post("/auth/signup", json={"email": "real@test.com", "password": "password123"})
    for _ in range(5):
        client.post(
            "/auth/login",
            json={"email": "real@test.com", "password": "wrongpass"},
            headers=_csrf_header(client),
        )
    res = client.post(
        "/auth/login",
        json={"email": "real@test.com", "password": "wrongpass"},
        headers=_csrf_header(client),
    )
    assert res.status_code == 429


def test_me_requires_auth_and_succeeds_with_cookie(db_session):
    client = TestClient(app)

    res = client.get("/auth/me")
    assert res.status_code == 401

    client.post("/auth/signup", json={"email": "d@test.com", "password": "password123"})
    res = client.get("/auth/me")
    assert res.status_code == 200
    assert res.json()["user"]["email"] == "d@test.com"


def test_logout_revokes_refresh_and_clears_cookies(db_session):
    client = TestClient(app)
    client.post("/auth/signup", json={"email": "e@test.com", "password": "password123"})
    res = client.post("/auth/logout", headers=_csrf_header(client))
    assert res.status_code == 200
    # refresh after logout should fail
    res = client.post("/auth/refresh", headers=_csrf_header(client))
    assert res.status_code == 401


def test_verify_invalid_token_returns_400(db_session):
    client = TestClient(app)
    res = client.post(
        "/auth/verify-email",
        json={"token": "bogus"},
        headers={"X-CSRF-Token": "t"},
    )
    assert res.status_code == 400


def test_refresh_expired_token_returns_401(db_session):
    client = TestClient(app)
    client.post("/auth/signup", json={"email": "f@test.com", "password": "password123"})
    refresh_token = client.cookies.get("refresh_token")

    # Expire the refresh token in the DB
    token_row = (
        db_session.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token)
        .first()
    )
    token_row.expires_at = datetime.now(timezone.utc) - timedelta(hours=1)
    db_session.commit()

    res = client.post("/auth/refresh", headers=_csrf_header(client))
    assert res.status_code == 401


def test_refresh_with_tampered_token_returns_401(db_session):
    client = TestClient(app)
    client.post("/auth/signup", json={"email": "g@test.com", "password": "password123"})
    tampered = client.cookies.get("refresh_token") + "tamper"
    # Set cookies on the client to avoid per-request cookies warning
    client.cookies.set("refresh_token", tampered)
    res = client.post("/auth/refresh", headers=_csrf_header(client))
    assert res.status_code == 401
