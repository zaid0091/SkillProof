"""Audit: Immutable security and administrative event log.

Phase 2 delivers the first slice of this module because authentication and
role changes must be auditable from the moment they exist (docs/phases.md
Phase 2, docs/sacs.md section 9). Administrative and moderation events from
later phases (SP-039) are appended to the same record.

Records are append-only: they can be written and read, never updated or
deleted through application code.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from common.models import UUIDPrimaryKeyModel


class AuditEvent(UUIDPrimaryKeyModel):
    """One immutable security or administrative event."""

    class Event(models.TextChoices):
        LOGIN_SUCCEEDED = "auth.login_succeeded", "Login succeeded"
        LOGIN_FAILED = "auth.login_failed", "Login failed"
        LOGOUT = "auth.logout", "Logout"
        TOKEN_REFRESH_FAILED = "auth.token_refresh_failed", "Token refresh failed"
        USER_REGISTERED = "auth.user_registered", "User registered"
        EMAIL_VERIFIED = "auth.email_verified", "Email verified"
        VERIFICATION_RESENT = "auth.verification_resent", "Verification email resent"
        PASSWORD_RESET_REQUESTED = "auth.password_reset_requested", "Password reset requested"
        PASSWORD_RESET_COMPLETED = "auth.password_reset_completed", "Password reset completed"
        PASSWORD_RESET_FAILED = "auth.password_reset_failed", "Password reset failed"
        ROLE_CHANGED = "auth.role_changed", "Role changed"

    class Outcome(models.TextChoices):
        SUCCESS = "success", "Success"
        FAILURE = "failure", "Failure"

    event = models.CharField(max_length=64, choices=Event.choices, db_index=True)
    outcome = models.CharField(
        max_length=16, choices=Outcome.choices, default=Outcome.SUCCESS, db_index=True
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_events",
        help_text="Authenticated actor, when known. Never deleted when the account goes away.",
    )
    actor_email = models.CharField(
        max_length=254,
        blank=True,
        help_text="Denormalised actor identifier so the record stays meaningful after account deletion.",
    )
    target = models.CharField(
        max_length=254,
        blank=True,
        help_text="Affected resource identifier (usually an email address).",
    )
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [models.Index(fields=["event", "created_at"])]

    def __str__(self) -> str:  # pragma: no cover - diagnostic helper
        return f"{self.event} ({self.outcome})"

    def save(self, *args, **kwargs):
        # Append-only: refuse to rewrite history once the row exists.
        if not self._state.adding:
            raise ValueError("Audit events are immutable and cannot be updated.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):  # pragma: no cover - safety guard
        raise ValueError("Audit events are immutable and cannot be deleted.")
