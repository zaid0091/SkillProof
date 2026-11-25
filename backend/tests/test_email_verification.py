"""Email verification: single-use, time-limited, and never state-disclosing."""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.utils import timezone
from rest_framework.test import APIClient

from apps.accounts.models import EmailVerificationToken, User
from apps.audit.models import AuditEvent

pytestmark = pytest.mark.django_db

REGISTER_URL = "/api/v1/auth/register/"
VERIFY_URL = "/api/v1/auth/verify-email/"
RESEND_URL = "/api/v1/auth/resend-verification/"
LOGIN_URL = "/api/v1/auth/login/"


@pytest.fixture
def unverified_user():
    return User.objects.create_user("ada@example.com", password="correct-horse-battery")


def issue_for(user) -> str:
    return EmailVerificationToken.issue(user, timedelta(hours=72))


def test_valid_token_verifies_the_account(unverified_user):
    raw = issue_for(unverified_user)

    response = APIClient().post(VERIFY_URL, {"token": raw}, format="json")

    assert response.status_code == 200
    unverified_user.refresh_from_db()
    assert unverified_user.is_verified is True
    assert AuditEvent.objects.filter(event=AuditEvent.Event.EMAIL_VERIFIED).exists()


def test_token_cannot_be_reused(unverified_user):
    raw = issue_for(unverified_user)
    APIClient().post(VERIFY_URL, {"token": raw}, format="json")

    response = APIClient().post(VERIFY_URL, {"token": raw}, format="json")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_token"


def test_expired_token_is_rejected(unverified_user):
    raw = issue_for(unverified_user)
    EmailVerificationToken.objects.filter(user=unverified_user).update(
        expires_at=timezone.now() - timedelta(minutes=1)
    )

    response = APIClient().post(VERIFY_URL, {"token": raw}, format="json")

    assert response.status_code == 400
    unverified_user.refresh_from_db()
    assert unverified_user.is_verified is False


def test_unknown_token_is_rejected():
    response = APIClient().post(VERIFY_URL, {"token": "made-up"}, format="json")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_token"


def test_invalid_and_expired_tokens_get_the_same_message(unverified_user):
    raw = issue_for(unverified_user)
    EmailVerificationToken.objects.filter(user=unverified_user).update(
        expires_at=timezone.now() - timedelta(minutes=1)
    )

    expired = APIClient().post(VERIFY_URL, {"token": raw}, format="json").json()["error"]
    unknown = APIClient().post(VERIFY_URL, {"token": "made-up"}, format="json").json()["error"]

    assert expired["message"] == unknown["message"]


def test_resend_issues_a_fresh_token(unverified_user):
    client = APIClient()
    client.force_authenticate(unverified_user)
    first = issue_for(unverified_user)

    response = client.post(RESEND_URL)

    assert response.status_code == 200
    assert EmailVerificationToken.objects.filter(user=unverified_user).count() == 2
    assert (
        EmailVerificationToken.objects.filter(user=unverified_user, used_at__isnull=True).count()
        == 2
    )
    assert first  # original token remains valid until it expires or is used


def test_resend_requires_authentication(unverified_user):
    response = APIClient().post(RESEND_URL)

    assert response.status_code == 401


def test_resend_rejects_verified_account(unverified_user):
    unverified_user.is_verified = True
    unverified_user.save(update_fields=["is_verified", "updated_at"])
    client = APIClient()
    client.force_authenticate(unverified_user)

    response = client.post(RESEND_URL)

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "already_verified"


def test_unverified_accounts_can_log_in_but_cannot_write():
    User.objects.create_user("ada@example.com", password="correct-horse-battery")
    client = APIClient()

    login = client.post(
        LOGIN_URL, {"email": "ada@example.com", "password": "correct-horse-battery"}, format="json"
    )
    assert login.status_code == 200  # reads stay available (build-plan 6.2)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.json()['access']}")

    # Sensitive writes require a verified email address.
    response = client.patch("/api/v1/auth/me/", {"full_name": "Ada"}, format="json")
    assert response.status_code == 403
    assert response.json()["error"]["code"] == "permission_denied"

    # The account can still read its own state.
    assert client.get("/api/v1/auth/me/").status_code == 200


def test_verification_flow_end_to_end():
    APIClient().post(
        REGISTER_URL,
        {"email": "ada@example.com", "password": "correct-horse-battery"},
        format="json",
    )
    user = User.objects.get(email="ada@example.com")
    assert EmailVerificationToken.objects.filter(user=user).count() == 1
    assert user.is_verified is False

    # The raw token is only delivered by email; take it from the message body.
    from django.core import mail

    body = mail.outbox[0].message().get_payload()
    raw = body.split("token=")[1].splitlines()[0].strip()

    response = APIClient().post(VERIFY_URL, {"token": raw}, format="json")

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_verified is True


def test_verified_account_can_update_profile():
    user = User.objects.create_user(
        "ada@example.com", password="correct-horse-battery", is_verified=True
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.patch("/api/v1/auth/me/", {"full_name": "Ada Lovelace"}, format="json")

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.full_name == "Ada Lovelace"
