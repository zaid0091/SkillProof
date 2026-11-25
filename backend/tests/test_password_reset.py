"""SP-008: password recovery.

Recovery must never reveal whether an email exists, tokens are time-limited
and single use, and a completed reset invalidates every existing session.
"""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.core import mail
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from apps.accounts.cookies import REFRESH_COOKIE_NAME
from apps.accounts.models import PasswordResetToken, User
from apps.accounts.roles import Role
from apps.audit.models import AuditEvent

pytestmark = pytest.mark.django_db

REQUEST_URL = "/api/v1/auth/password-reset/"
CONFIRM_URL = "/api/v1/auth/password-reset/confirm/"
LOGIN_URL = "/api/v1/auth/login/"
ME_URL = "/api/v1/auth/me/"


@pytest.fixture
def user():
    return User.objects.create_user("ada@example.com", password="correct-horse-battery")


def request_reset(client: APIClient, email: str):
    return client.post(REQUEST_URL, {"email": email}, format="json")


def test_unknown_email_gets_the_same_response_as_a_known_one(user):
    known = request_reset(APIClient(), "ada@example.com")
    unknown = request_reset(APIClient(), "nobody@example.com")

    assert known.status_code == unknown.status_code == 200
    assert known.json() == unknown.json()  # no account-existence oracle
    assert mail.outbox[0].to == ["ada@example.com"]  # only the real account is mailed


def test_request_creates_a_single_use_token(user):
    request_reset(APIClient(), "ada@example.com")

    token = PasswordResetToken.objects.get(user=user)
    assert token.used_at is None
    assert token.expires_at > timezone.now()


def test_request_is_audited_even_for_unknown_emails(user):
    request_reset(APIClient(), "ada@example.com")
    request_reset(APIClient(), "nobody@example.com")

    events = AuditEvent.objects.filter(event=AuditEvent.Event.PASSWORD_RESET_REQUESTED)
    assert events.filter(outcome=AuditEvent.Outcome.SUCCESS, target="ada@example.com").exists()
    assert events.filter(outcome=AuditEvent.Outcome.FAILURE, target="nobody@example.com").exists()


def test_confirm_updates_password_and_signs_out_every_session(user):
    # Two sessions exist before the reset.
    for _ in range(2):
        APIClient().post(
            LOGIN_URL,
            {"email": "ada@example.com", "password": "correct-horse-battery"},
            format="json",
        )
    assert OutstandingToken.objects.filter(user=user).count() == 2

    raw = PasswordResetToken.issue(user, timedelta(minutes=60))
    response = APIClient().post(
        CONFIRM_URL, {"token": raw, "new_password": "brand-new-passphrase"}, format="json"
    )

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password("brand-new-passphrase")
    assert BlacklistedToken.objects.count() == 2  # every session revoked
    assert AuditEvent.objects.filter(event=AuditEvent.Event.PASSWORD_RESET_COMPLETED).exists()


def test_confirm_token_cannot_be_reused(user):
    raw = PasswordResetToken.issue(user, timedelta(minutes=60))
    APIClient().post(
        CONFIRM_URL, {"token": raw, "new_password": "brand-new-passphrase"}, format="json"
    )

    response = APIClient().post(
        CONFIRM_URL, {"token": raw, "new_password": "third-good-passphrase"}, format="json"
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_token"
    user.refresh_from_db()
    assert user.check_password("brand-new-passphrase")  # unchanged by the replay


def test_expired_token_is_rejected(user):
    raw = PasswordResetToken.issue(user, timedelta(minutes=60))
    PasswordResetToken.objects.filter(user=user).update(
        expires_at=timezone.now() - timedelta(minutes=1)
    )

    response = APIClient().post(
        CONFIRM_URL, {"token": raw, "new_password": "brand-new-passphrase"}, format="json"
    )

    assert response.status_code == 400
    user.refresh_from_db()
    assert user.check_password("correct-horse-battery")


def test_invalid_token_and_expired_token_get_the_same_message(user):
    raw = PasswordResetToken.issue(user, timedelta(minutes=60))
    PasswordResetToken.objects.filter(user=user).update(
        expires_at=timezone.now() - timedelta(minutes=1)
    )

    expired = (
        APIClient()
        .post(CONFIRM_URL, {"token": raw, "new_password": "brand-new-passphrase"}, format="json")
        .json()["error"]
    )
    unknown = (
        APIClient()
        .post(
            CONFIRM_URL, {"token": "made-up", "new_password": "brand-new-passphrase"}, format="json"
        )
        .json()["error"]
    )

    assert expired["message"] == unknown["message"]


def test_confirm_enforces_the_password_policy(user):
    raw = PasswordResetToken.issue(user, timedelta(minutes=60))

    response = APIClient().post(CONFIRM_URL, {"token": raw, "new_password": "tiny"}, format="json")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    # The token was not consumed by a failed attempt.
    assert PasswordResetToken.objects.get(user=user).used_at is None


def test_confirm_invalidates_other_outstanding_reset_links(user):
    first = PasswordResetToken.issue(user, timedelta(minutes=60))
    second = PasswordResetToken.issue(user, timedelta(minutes=60))

    APIClient().post(
        CONFIRM_URL, {"token": first, "new_password": "brand-new-passphrase"}, format="json"
    )

    response = APIClient().post(
        CONFIRM_URL, {"token": second, "new_password": "another-passphrase"}, format="json"
    )
    assert response.status_code == 400


def test_old_password_stops_working_after_reset(user):
    raw = PasswordResetToken.issue(user, timedelta(minutes=60))
    APIClient().post(
        CONFIRM_URL, {"token": raw, "new_password": "brand-new-passphrase"}, format="json"
    )

    old_login = APIClient().post(
        LOGIN_URL,
        {"email": "ada@example.com", "password": "correct-horse-battery"},
        format="json",
    )
    assert old_login.status_code == 401

    new_login = APIClient().post(
        LOGIN_URL,
        {"email": "ada@example.com", "password": "brand-new-passphrase"},
        format="json",
    )
    assert new_login.status_code == 200
    assert REFRESH_COOKIE_NAME in new_login.cookies


def test_reset_does_not_accept_admin_password_changes_by_proxy(user):
    # A reset only ever affects the account that owns the token.
    other = User.objects.create_user("grace@example.com", password="original-passphrase")
    raw = PasswordResetToken.issue(user, timedelta(minutes=60))

    APIClient().post(
        CONFIRM_URL, {"token": raw, "new_password": "brand-new-passphrase"}, format="json"
    )

    other.refresh_from_db()
    assert other.check_password("original-passphrase")
    assert other.role == Role.STUDENT
