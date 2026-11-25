"""SP-007: role-based access control and its audit trail."""

from __future__ import annotations

import pytest
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from apps.accounts.models import User
from apps.accounts.roles import Role
from apps.audit.models import AuditEvent
from common.permissions import (
    HasRole,
    IsAdministrator,
    IsEmployer,
    IsOwner,
    IsStudent,
    IsUniversity,
    IsVerifiedUser,
    ReadOnly,
)

pytestmark = pytest.mark.django_db

factory = APIRequestFactory()


class ProbeView(APIView):
    authentication_classes: list = []
    permission_classes: list = []

    def get(self, request):
        return Response({"status": "ok"})


def request_for(user, method: str = "get"):
    request = getattr(factory, method)("/")
    request.user = user
    return request


def check(permission_cls, user, obj=None, method: str = "get") -> bool:
    view = ProbeView()
    permission = permission_cls()
    request = request_for(user, method)
    if not permission.has_permission(request, view):
        return False
    return obj is None or permission.has_object_permission(request, view, obj)


def test_role_permissions_match_the_assigned_role():
    student = User.objects.create_user("s@example.com", password="x-long-enough", role=Role.STUDENT)
    employer = User.objects.create_user(
        "e@example.com", password="x-long-enough", role=Role.EMPLOYER
    )
    university = User.objects.create_user(
        "u@example.com", password="x-long-enough", role=Role.UNIVERSITY
    )
    admin = User.objects.create_user(
        "a@example.com", password="x-long-enough", role=Role.ADMINISTRATOR
    )

    assert check(IsStudent, student) and not check(IsStudent, employer)
    assert check(IsEmployer, employer) and not check(IsEmployer, student)
    assert check(IsUniversity, university) and not check(IsUniversity, employer)
    assert check(IsAdministrator, admin) and not check(IsAdministrator, student)


def test_cross_role_access_is_denied():
    student = User.objects.create_user("s@example.com", password="x-long-enough", role=Role.STUDENT)
    employer = User.objects.create_user(
        "e@example.com", password="x-long-enough", role=Role.EMPLOYER
    )

    # An employer cannot act as a student and vice versa.
    assert not check(IsStudent, employer)
    assert not check(IsEmployer, student)
    # Both are denied an administrator surface.
    assert not check(IsAdministrator, student)
    assert not check(IsAdministrator, employer)


def test_anonymous_and_inactive_users_are_denied():
    from django.contrib.auth.models import AnonymousUser

    anon = AnonymousUser()
    assert not check(IsStudent, anon)

    inactive = User.objects.create_user("i@example.com", password="x-long-enough")
    inactive.is_active = False
    assert not check(HasRole, inactive)


def test_is_owner_grants_only_the_owner():
    class Owned:
        def __init__(self, owner):
            self.user = owner

    ada = User.objects.create_user("ada@example.com", password="x-long-enough")
    grace = User.objects.create_user("grace@example.com", password="x-long-enough")
    record = Owned(ada)

    assert check(IsOwner, ada, obj=record)
    assert not check(IsOwner, grace, obj=record)


def test_verified_user_requires_verified_email():
    unverified = User.objects.create_user("u@example.com", password="x-long-enough")
    verified = User.objects.create_user("v@example.com", password="x-long-enough", is_verified=True)

    assert not check(IsVerifiedUser, unverified)
    assert check(IsVerifiedUser, verified)


def test_read_only_blocks_unsafe_methods():
    admin = User.objects.create_user(
        "a@example.com", password="x-long-enough", role=Role.ADMINISTRATOR
    )

    assert check(ReadOnly, admin, method="get")
    assert not check(ReadOnly, admin, method="post")


def test_organization_membership_denies_until_phase_three():
    """Fail closed: org membership lookup arrives in Phase 3 (SP-027/SP-031)."""
    from common.permissions import IsOrganizationMember

    employer = User.objects.create_user(
        "e@example.com", password="x-long-enough", role=Role.EMPLOYER
    )

    assert not check(IsOrganizationMember, employer)


def test_role_changes_are_audited():
    user = User.objects.create_user("ada@example.com", password="x-long-enough")
    assert not AuditEvent.objects.filter(event=AuditEvent.Event.ROLE_CHANGED).exists()

    user.role = Role.EMPLOYER
    user.save()

    event = AuditEvent.objects.get(event=AuditEvent.Event.ROLE_CHANGED)
    assert event.target == "ada@example.com"
    assert event.metadata == {"from": Role.STUDENT, "to": Role.EMPLOYER}

    # Unchanged saves do not spam the log.
    user.save()
    assert AuditEvent.objects.filter(event=AuditEvent.Event.ROLE_CHANGED).count() == 1


def test_audit_events_are_immutable():
    user = User.objects.create_user("ada@example.com", password="x-long-enough")
    event = AuditEvent.objects.create(event=AuditEvent.Event.LOGIN_SUCCEEDED, actor=user)

    with pytest.raises(ValueError):
        event.outcome = AuditEvent.Outcome.FAILURE
        event.save()
    with pytest.raises(ValueError):
        event.delete()
