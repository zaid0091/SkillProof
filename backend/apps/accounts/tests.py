"""Account model behaviour that later phases depend on."""

from __future__ import annotations

import pytest
from django.db import IntegrityError

from apps.accounts.models import User
from apps.accounts.roles import Role

pytestmark = pytest.mark.django_db


def test_create_user_normalises_email_and_defaults_to_student():
    user = User.objects.create_user("  Ada@Example.COM ", password="correct-horse")

    assert user.email == "ada@example.com"
    assert user.role == Role.STUDENT
    assert user.is_active is True
    assert user.is_verified is False
    assert user.check_password("correct-horse")
    assert user.display_name == "ada"


def test_duplicate_email_is_rejected_case_insensitively():
    User.objects.create_user("ada@example.com", password="correct-horse")

    with pytest.raises(IntegrityError):
        User.objects.create_user("ADA@example.com", password="another-password")


def test_superuser_gets_admin_role_and_verification():
    admin = User.objects.create_superuser("admin@example.com", password="correct-horse")

    assert admin.role == Role.ADMINISTRATOR
    assert admin.is_staff is True
    assert admin.is_superuser is True
    assert admin.is_verified is True


def test_user_requires_an_email():
    with pytest.raises(ValueError):
        User.objects.create_user("", password="correct-horse")


def test_display_name_falls_back_to_local_part():
    user = User(email="grace.hopper@example.com", full_name="")

    assert user.display_name == "grace.hopper"
