"""Role and object-level permission primitives.

These are building blocks, not a security boundary by themselves. Every view
still has to scope querysets to the caller; a permission class cannot stop a
view from returning someone else's record.

docs/sacs.md section 4: hiding UI is not authorization. The backend must verify
authentication, role, resource ownership, and the resource's current state.
"""

from __future__ import annotations

from typing import Any

from rest_framework.permissions import SAFE_METHODS, BasePermission

from apps.accounts.roles import Role


class HasRole(BasePermission):
    """Authenticated user whose primary role is in ``allowed_roles``."""

    allowed_roles: tuple[str, ...] = ()
    message = "Your account role does not permit this action."

    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and user.is_active
            and getattr(user, "role", None) in self.allowed_roles
        )


class IsStudent(HasRole):
    allowed_roles = (Role.STUDENT,)


class IsEmployer(HasRole):
    allowed_roles = (Role.EMPLOYER,)


class IsUniversity(HasRole):
    allowed_roles = (Role.UNIVERSITY,)


class IsAdministrator(HasRole):
    allowed_roles = (Role.ADMINISTRATOR,)


class IsVerifiedUser(BasePermission):
    """Account has completed email verification (required for sensitive writes)."""

    message = "Verify your email address before using this feature."

    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "is_verified", False))


class IsOwner(BasePermission):
    """Object-level check against an owner field.

    Set ``owner_field`` on the view (defaults to "user").
    """

    message = "You do not have access to this record."

    def has_object_permission(self, request, view, obj: Any) -> bool:
        field = getattr(view, "owner_field", "user")
        return getattr(obj, field, None) == request.user


class IsOrganizationMember(BasePermission):
    """Organization-scoped access control.

    Phase 3 (SP-027, SP-031) implements membership lookup. Until then this class
    denies access explicitly rather than silently allowing it.
    """

    message = "You are not a member of this organization."

    def has_permission(self, request, view) -> bool:
        return False

    def has_object_permission(self, request, view, obj: Any) -> bool:
        return False


class ReadOnly(BasePermission):
    """Allow only safe methods (GET, HEAD, OPTIONS)."""

    def has_permission(self, request, view) -> bool:
        return request.method in SAFE_METHODS
