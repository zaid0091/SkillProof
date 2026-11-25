"""SP-005: registration contract.

Registration must validate input, reject duplicates, hash passwords, never
accept privileged roles, and never leak sensitive fields in responses.
"""

from __future__ import annotations

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import EmailVerificationToken, User
from apps.accounts.roles import Role
from apps.audit.models import AuditEvent

pytestmark = pytest.mark.django_db

REGISTER_URL = "/api/v1/auth/register/"


def test_registration_creates_account_with_hashed_password():
    response = APIClient().post(
        REGISTER_URL,
        {"email": "Ada@Example.com", "password": "correct-horse-battery", "full_name": "Ada"},
        format="json",
    )

    assert response.status_code == 201
    user = User.objects.get(email="ada@example.com")
    assert user.role == Role.STUDENT
    assert user.is_verified is False
    assert user.check_password("correct-horse-battery")
    assert not user.password.startswith("correct-horse")

    body = response.json()
    assert body["user"]["email"] == "ada@example.com"
    assert body["user"]["role"] == Role.STUDENT
    # No secrets in the public response.
    assert "password" not in body["user"]
    assert "access" not in body
    assert "refresh" not in body


def test_registration_rejects_duplicate_email_case_insensitively():
    User.objects.create_user("ada@example.com", password="correct-horse-battery")

    response = APIClient().post(
        REGISTER_URL,
        {"email": "ADA@example.com", "password": "another-good-pass"},
        format="json",
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    assert User.objects.count() == 1


def test_registration_rejects_weak_password():
    response = APIClient().post(
        REGISTER_URL,
        {"email": "ada@example.com", "password": "short"},
        format="json",
    )

    assert response.status_code == 400
    body = response.json()["error"]
    assert body["code"] == "validation_error"
    assert "password" in body["details"]
    assert not User.objects.exists()


def test_registration_rejects_invalid_email():
    response = APIClient().post(
        REGISTER_URL,
        {"email": "not-an-email", "password": "correct-horse-battery"},
        format="json",
    )

    assert response.status_code == 400
    assert not User.objects.exists()


@pytest.mark.parametrize("privileged_role", ["administrator", "admin", "ADMINISTRATOR"])
def test_privileged_roles_cannot_be_self_assigned(privileged_role):
    response = APIClient().post(
        REGISTER_URL,
        {
            "email": "mallory@example.com",
            "password": "correct-horse-battery",
            "role": privileged_role,
        },
        format="json",
    )

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "validation_error"
    assert not User.objects.filter(email="mallory@example.com").exists()


def test_unknown_roles_are_rejected():
    response = APIClient().post(
        REGISTER_URL,
        {
            "email": "mallory@example.com",
            "password": "correct-horse-battery",
            "role": "superuser",
        },
        format="json",
    )

    assert response.status_code == 400
    assert not User.objects.exists()


def test_self_assignable_roles_are_accepted():
    response = APIClient().post(
        REGISTER_URL,
        {
            "email": "hire@example.com",
            "password": "correct-horse-battery",
            "role": "employer",
        },
        format="json",
    )

    assert response.status_code == 201
    assert User.objects.get(email="hire@example.com").role == Role.EMPLOYER


def test_registration_sends_single_use_verification_token():
    APIClient().post(
        REGISTER_URL,
        {"email": "ada@example.com", "password": "correct-horse-battery"},
        format="json",
    )

    user = User.objects.get(email="ada@example.com")
    token = EmailVerificationToken.objects.get(user=user)
    assert token.used_at is None
    assert token.expires_at > token.created_at
    # Only a hash is stored; the raw token never lands in the database.
    assert len(token.token_hash) == 64


def test_registration_is_audited():
    APIClient().post(
        REGISTER_URL,
        {"email": "ada@example.com", "password": "correct-horse-battery"},
        format="json",
    )

    event = AuditEvent.objects.get(event=AuditEvent.Event.USER_REGISTERED)
    assert event.target == "ada@example.com"
    assert event.metadata["role"] == Role.STUDENT
