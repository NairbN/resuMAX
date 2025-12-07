import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import app
from app.services import auth as auth_service


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
