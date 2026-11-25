"""SP-006: login, JWT handling, refresh rotation, and logout."""

from __future__ import annotations

from datetime import timedelta

import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.cookies import REFRESH_COOKIE_NAME
from apps.accounts.models import User
from apps.audit.models import AuditEvent

pytestmark = pytest.mark.django_db

LOGIN_URL = "/api/v1/auth/login/"
REFRESH_URL = "/api/v1/auth/token/refresh/"
LOGOUT_URL = "/api/v1/auth/logout/"
ME_URL = "/api/v1/auth/me/"


@pytest.fixture
def user():
    return User.objects.create_user("ada@example.com", password="correct-horse-battery")


def login(client: APIClient, email: str, password: str):
    response = client.post(LOGIN_URL, {"email": email, "password": password}, format="json")
    if response.status_code == 200:
        # Mirror the browser: keep the access token in memory and send it as a
        # bearer header; the refresh token travels in the client's cookie jar.
        client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.json()['access']}")
    return response


def test_login_with_valid_credentials_returns_access_token(user):
    client = APIClient()
    response = login(client, "ada@example.com", "correct-horse-battery")

    assert response.status_code == 200
    body = response.json()
    assert body["access"]
    assert body["user"]["email"] == "ada@example.com"
    assert "refresh" not in body  # refresh lives only in the HttpOnly cookie
    assert REFRESH_COOKIE_NAME in response.cookies
    assert response.cookies[REFRESH_COOKIE_NAME]["httponly"] is True


def test_login_rejects_wrong_password(user):
    response = login(APIClient(), "ada@example.com", "wrong-password")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_credentials"


def test_login_rejects_unknown_account():
    response = login(APIClient(), "nobody@example.com", "correct-horse-battery")

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_credentials"


def test_login_rejects_inactive_account(user):
    user.is_active = False
    user.save(update_fields=["is_active", "updated_at"])

    response = login(APIClient(), "ada@example.com", "correct-horse-battery")

    assert response.status_code == 401


def test_login_attempts_are_audited(user):
    client = APIClient()
    login(client, "ada@example.com", "wrong-password")
    login(client, "ada@example.com", "correct-horse-battery")

    assert AuditEvent.objects.filter(
        event=AuditEvent.Event.LOGIN_FAILED, outcome=AuditEvent.Outcome.FAILURE
    ).exists()
    assert AuditEvent.objects.filter(event=AuditEvent.Event.LOGIN_SUCCEEDED).exists()


def test_protected_endpoint_rejects_anonymous_requests():
    response = APIClient().get(ME_URL)

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "not_authenticated"


def test_protected_endpoint_rejects_invalid_token():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION="Bearer not-a-real-token")

    response = client.get(ME_URL)

    assert response.status_code == 401
    assert response.json()["error"]["code"] in ("authentication_failed", "not_authenticated")


def test_protected_endpoint_rejects_expired_token(user):
    expired_access = RefreshToken.for_user(user).access_token
    expired_access.set_exp(lifetime=timedelta(seconds=-60))  # already expired
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {expired_access}")

    response = client.get(ME_URL)

    assert response.status_code == 401


def test_me_returns_the_authenticated_account(user):
    client = APIClient()
    login(client, "ada@example.com", "correct-horse-battery")

    response = client.get(ME_URL)

    assert response.status_code == 200
    assert response.json()["user"]["email"] == "ada@example.com"


def test_refresh_rotates_tokens_and_returns_new_access(user):
    client = APIClient()
    login(client, "ada@example.com", "correct-horse-battery")
    first_cookie = client.cookies[REFRESH_COOKIE_NAME].value

    response = client.post(REFRESH_URL)

    assert response.status_code == 200
    assert response.json()["access"]
    new_cookie = response.cookies[REFRESH_COOKIE_NAME].value
    assert new_cookie != first_cookie  # rotation

    # The rotated-out token is dead.
    with pytest.raises(TokenError):
        RefreshToken(first_cookie)


def test_refresh_rejects_garbage_token():
    client = APIClient()
    client.cookies[REFRESH_COOKIE_NAME] = "garbage"

    response = client.post(REFRESH_URL)

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_refresh_token"
    assert response.cookies[REFRESH_COOKIE_NAME].value == ""  # cookie cleared


def test_refresh_without_any_token_is_rejected():
    response = APIClient().post(REFRESH_URL)

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "not_authenticated"


def test_refresh_from_untrusted_origin_is_rejected(user):
    client = APIClient()
    login(client, "ada@example.com", "correct-horse-battery")

    response = client.post(REFRESH_URL, HTTP_ORIGIN="https://evil.example")

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "permission_denied"


def test_refresh_accepts_token_from_trusted_origin(user):
    client = APIClient()
    login(client, "ada@example.com", "correct-horse-battery")

    response = client.post(REFRESH_URL, HTTP_ORIGIN="http://localhost:3000")

    assert response.status_code == 200


def test_logout_blacklists_the_session(user):
    client = APIClient()
    login(client, "ada@example.com", "correct-horse-battery")
    refresh = client.cookies[REFRESH_COOKIE_NAME].value
    jti = RefreshToken(refresh).payload["jti"]

    response = client.post(LOGOUT_URL)

    assert response.status_code == 200
    assert response.cookies[REFRESH_COOKIE_NAME].value == ""
    assert BlacklistedToken.objects.filter(token__jti=jti).exists()

    # Replaying the logged-out token fails.
    replay = APIClient()
    replay.cookies[REFRESH_COOKIE_NAME] = refresh
    assert replay.post(REFRESH_URL).status_code == 401


def test_logout_without_a_session_still_succeeds(user):
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(LOGOUT_URL)

    assert response.status_code == 200
    assert AuditEvent.objects.filter(event=AuditEvent.Event.LOGOUT).exists()
