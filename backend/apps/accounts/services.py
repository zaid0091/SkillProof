"""Account workflows: registration, verification, login, and recovery.

Views stay thin; the rules live here so they can be reused and tested without
HTTP. Every security-relevant outcome is written to the audit log
(docs/sacs.md section 9.1).
"""

from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts import emails
from apps.accounts.models import EmailVerificationToken, PasswordResetToken, User
from apps.accounts.roles import Role
from apps.audit import services as audit_services
from apps.audit.models import AuditEvent
from common.exceptions import ApiError

REGISTRABLE_ROLES = (Role.STUDENT, Role.EMPLOYER, Role.UNIVERSITY)


def _verification_ttl() -> timedelta:
    return timedelta(hours=settings.EMAIL_VERIFICATION_TOKEN_TTL_HOURS)


def _password_reset_ttl() -> timedelta:
    return timedelta(minutes=settings.PASSWORD_RESET_TOKEN_TTL_MINUTES)


def issue_tokens(user) -> tuple[str, str]:
    """Return (access_token, refresh_token) for an active user."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


def blacklist_refresh_token(raw_token: str) -> bool:
    """Blacklist one refresh token. Returns False when the token is unknown."""
    try:
        refresh = RefreshToken(raw_token)
    except TokenError:
        return False
    jti = refresh.payload.get("jti")
    outstanding = OutstandingToken.objects.filter(jti=jti).first()
    if outstanding is None:
        return False
    BlacklistedToken.objects.get_or_create(token=outstanding)
    return True


def invalidate_all_sessions(user) -> None:
    """Blacklist every outstanding refresh token for ``user`` (sign out everywhere)."""
    for outstanding in OutstandingToken.objects.filter(user=user):
        BlacklistedToken.objects.get_or_create(token=outstanding)


# --- Registration and verification ------------------------------------------


def register_user(*, email: str, password: str, full_name: str = "", role: str = Role.STUDENT):
    """Create an account and send its email-verification link.

    Role is validated here as well as at the serializer boundary: privileged
    roles can never be assigned through registration (docs/sacs.md section 3.1).
    """
    if role not in REGISTRABLE_ROLES:
        raise ApiError(
            "role_not_allowed",
            "Privileged roles cannot be assigned during registration.",
            status_code=403,
        )
    user = User.objects.create_user(email=email, password=password, full_name=full_name, role=role)
    raw_token = EmailVerificationToken.issue(user, _verification_ttl())
    emails.send_verification_email(user, raw_token)
    audit_services.record(
        AuditEvent.Event.USER_REGISTERED, actor=user, target=user.email, metadata={"role": role}
    )
    return user


def verify_email(raw_token: str) -> User:
    token = EmailVerificationToken.consume(raw_token)
    if token is None:
        raise ApiError(
            "invalid_token",
            "This verification link is invalid or has expired.",
            status_code=400,
        )
    user = token.user
    if not user.is_verified:
        user.is_verified = True
        user.save(update_fields=["is_verified", "updated_at"])
    audit_services.record(AuditEvent.Event.EMAIL_VERIFIED, actor=user, target=user.email)
    return user


def resend_verification(user) -> None:
    if user.is_verified:
        raise ApiError(
            "already_verified",
            "This email address is already verified.",
            status_code=400,
        )
    raw_token = EmailVerificationToken.issue(user, _verification_ttl())
    emails.send_verification_email(user, raw_token)
    audit_services.record(AuditEvent.Event.VERIFICATION_RESENT, actor=user, target=user.email)


# --- Login ------------------------------------------------------------------


def login(*, email: str, password: str):
    """Authenticate and return (user, access, refresh).

    Failure is always the same client-facing error; the audit log keeps the
    real reason for operators.
    """
    user = authenticate(username=email, password=password)
    if user is None:
        reason = "unknown_account"
        if User.objects.filter(email=email.lower().strip()).exists():
            reason = "bad_credentials_or_inactive"
        audit_services.record(
            AuditEvent.Event.LOGIN_FAILED,
            target=email.lower().strip(),
            outcome=AuditEvent.Outcome.FAILURE,
            metadata={"reason": reason},
        )
        raise ApiError("invalid_credentials", "Invalid email or password.", status_code=401)
    access, refresh = issue_tokens(user)
    audit_services.record(AuditEvent.Event.LOGIN_SUCCEEDED, actor=user, target=user.email)
    return user, access, refresh


# --- Password recovery ------------------------------------------------------


def request_password_reset(email: str) -> None:
    """Send a reset link if the account exists; never reveal whether it does."""
    normalised = (email or "").lower().strip()
    user = User.objects.filter(email=normalised, is_active=True).first()
    if user is None:
        audit_services.record(
            AuditEvent.Event.PASSWORD_RESET_REQUESTED,
            target=normalised,
            outcome=AuditEvent.Outcome.FAILURE,
            metadata={"reason": "no_matching_active_account"},
        )
        return
    raw_token = PasswordResetToken.issue(user, _password_reset_ttl())
    emails.send_password_reset_email(user, raw_token)
    audit_services.record(AuditEvent.Event.PASSWORD_RESET_REQUESTED, actor=user, target=user.email)


def confirm_password_reset(*, raw_token: str, new_password: str) -> User:
    token = PasswordResetToken.consume(raw_token)
    if token is None:
        audit_services.record(
            AuditEvent.Event.PASSWORD_RESET_FAILED,
            outcome=AuditEvent.Outcome.FAILURE,
            metadata={"reason": "invalid_or_expired_token"},
        )
        raise ApiError(
            "invalid_token",
            "This password reset link is invalid or has expired.",
            status_code=400,
        )
    user = token.user
    user.set_password(new_password)
    user.save(update_fields=["password", "updated_at"])
    # Single use everywhere: other outstanding reset links die with this one.
    PasswordResetToken.invalidate_outstanding(user)
    # A password change signs out every existing session (docs/sacs.md 3.5).
    invalidate_all_sessions(user)
    emails.send_password_changed_notification(user)
    audit_services.record(AuditEvent.Event.PASSWORD_RESET_COMPLETED, actor=user, target=user.email)
    return user
