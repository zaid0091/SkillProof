"""User identity and role.

The custom user model is introduced in Phase 1 — before any other module has
migrations — because swapping AUTH_USER_MODEL later is a destructive migration.
Additional account features (verification tokens, login throttling, password
recovery) are delivered in Phase 2 and do not require replacing this model.

docs/tad.md section 6.2 specifies the fields. Role assignment is owned by the
backend and must never be accepted from a registration payload
(docs/sacs.md section 3.1).
"""

from __future__ import annotations

import hashlib
import secrets
import uuid

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.accounts.roles import Role
from common.models import BaseModel


class UserManager(BaseUserManager):
    """Email-based user creation. Emails are the login identifier."""

    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.full_clean(exclude=["password"])
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("role", Role.STUDENT)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str | None = None, **extra_fields):
        extra_fields.setdefault("role", Role.ADMINISTRATOR)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("A superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Platform account for students, employers, universities, and admins."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("email address", unique=True, db_index=True)
    full_name = models.CharField(max_length=150, blank=True)

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        db_index=True,
        help_text="Primary platform role. Assigned by the backend, not the client.",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Unset to suspend the account without deleting its history.",
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Email address has been confirmed.",
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="May access the Django administration site.",
    )

    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = []

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ("-date_joined",)
        indexes = [
            models.Index(fields=["role", "is_active"]),
        ]

    def __str__(self) -> str:
        return self.email

    @property
    def display_name(self) -> str:
        return self.full_name or self.email.split("@")[0]

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super().from_db(db, field_names, values)
        # Snapshot the stored role so save() can detect privileged role changes.
        instance._loaded_role = instance.role
        return instance

    def save(self, *args, **kwargs):
        # Normalising here protects paths that bypass UserManager (for example the
        # admin or a future bulk import) from creating duplicate accounts that
        # differ only by letter case.
        self.email = self.email.lower().strip()
        previous_role = getattr(self, "_loaded_role", None)
        super().save(*args, **kwargs)
        self._loaded_role = self.role
        if previous_role is not None and previous_role != self.role:
            # Role assignment/removal is audited (docs/sacs.md section 9.1).
            from apps.audit import services as audit_services
            from apps.audit.models import AuditEvent

            audit_services.record(
                AuditEvent.Event.ROLE_CHANGED,
                actor=self,
                target=self.email,
                metadata={"from": previous_role, "to": self.role},
            )


class OneTimeToken(BaseModel):
    """A hashed, time-limited, single-use token issued to a user.

    Only the SHA-256 hash of the token is stored, so a database leak does not
    leak usable links. The raw token is delivered out of band (email) and
    checked exactly once through :meth:`consume`.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_set",
    )
    token_hash = models.CharField(max_length=64, unique=True, db_index=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:  # pragma: no cover - diagnostic helper
        return f"{type(self).__name__} for {self.user_id}"

    @staticmethod
    def hash_token(raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()

    @classmethod
    def issue(cls, user, ttl) -> str:
        """Create a token for ``user`` valid for ``ttl`` (timedelta); return the raw value."""
        raw_token = secrets.token_urlsafe(32)
        cls.objects.create(
            user=user,
            token_hash=cls.hash_token(raw_token),
            expires_at=timezone.now() + ttl,
        )
        return raw_token

    @classmethod
    def consume(cls, raw_token: str):
        """Mark a valid unused token as used and return it, or None if invalid/expired.

        Invalid, expired, and already-used tokens are indistinguishable to the
        caller by design: the API must not disclose token state.
        """
        if not raw_token:
            return None
        token = (
            cls.objects.filter(
                token_hash=cls.hash_token(raw_token),
                used_at__isnull=True,
                expires_at__gt=timezone.now(),
            )
            .select_related("user")
            .first()
        )
        if token is None:
            return None
        token.used_at = timezone.now()
        token.save(update_fields=["used_at"])
        return token

    @classmethod
    def invalidate_outstanding(cls, user) -> None:
        """Mark every unused token for ``user`` as used (e.g. after a password change)."""
        cls.objects.filter(user=user, used_at__isnull=True).update(used_at=timezone.now())


class EmailVerificationToken(OneTimeToken):
    """Single-use token proving control of an email address (Phase 2)."""

    class Meta:
        verbose_name = "email verification token"
        verbose_name_plural = "email verification tokens"


class PasswordResetToken(OneTimeToken):
    """Single-use token authorising one password reset (Phase 2)."""

    class Meta:
        verbose_name = "password reset token"
        verbose_name_plural = "password reset tokens"
