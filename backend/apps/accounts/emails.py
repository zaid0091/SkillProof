"""Account lifecycle emails.

Development uses the console email backend, so links are printed to the API
log; deployed environments configure SMTP. Messages contain only single-use
links, never credentials or tokens in plaintext beyond the link itself.
"""

from __future__ import annotations

from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(user, raw_token: str) -> None:
    link = f"{settings.FRONTEND_URL}/verify-email?token={raw_token}"
    send_mail(
        subject="Verify your SkillProof email address",
        message=(
            f"Hi {user.display_name},\n\n"
            "Confirm your SkillProof account by opening this link:\n\n"
            f"{link}\n\n"
            f"The link expires in {settings.EMAIL_VERIFICATION_TOKEN_TTL_HOURS} hours "
            "and can be used once.\n\n"
            "If you did not create a SkillProof account, you can ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def send_password_reset_email(user, raw_token: str) -> None:
    link = f"{settings.FRONTEND_URL}/reset-password?token={raw_token}"
    send_mail(
        subject="Reset your SkillProof password",
        message=(
            f"Hi {user.display_name},\n\n"
            "Choose a new password by opening this link:\n\n"
            f"{link}\n\n"
            f"The link expires in {settings.PASSWORD_RESET_TOKEN_TTL_MINUTES} minutes "
            "and can be used once.\n\n"
            "If you did not request a password reset, you can ignore this email "
            "and your password will stay unchanged."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )


def send_password_changed_notification(user) -> None:
    send_mail(
        subject="Your SkillProof password was changed",
        message=(
            f"Hi {user.display_name},\n\n"
            "The password for your SkillProof account was just changed and all "
            "other sessions were signed out.\n\n"
            "If this was not you, reset your password immediately."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
