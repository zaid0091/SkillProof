"""Account API serializers.

Passwords and tokens never leave the API in a response body. The registration
serializer accepts only self-assignable roles; privileged roles are rejected
with an explicit error rather than silently ignored (docs/sacs.md section 3.1).
"""

from __future__ import annotations

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.roles import Role
from apps.accounts.services import REGISTRABLE_ROLES


class UserSerializer(serializers.ModelSerializer):
    """Public account representation shared by auth responses."""

    display_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "display_name", "role", "is_verified", "date_joined")
        read_only_fields = fields


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    full_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    role = serializers.CharField(required=False, default=Role.STUDENT)

    def validate_email(self, value: str) -> str:
        email = value.lower().strip()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("An account with this email address already exists.")
        return email

    def validate_password(self, value: str) -> str:
        # Uses the platform password policy from settings (min length 10, etc.).
        validate_password(value)
        return value

    def validate_role(self, value: str) -> str:
        role = (value or "").lower().strip()
        if role == Role.ADMINISTRATOR:
            raise serializers.ValidationError(
                "Privileged roles cannot be assigned during registration."
            )
        if role not in REGISTRABLE_ROLES:
            raise serializers.ValidationError(
                "Choose one of the available account types: student, employer, university."
            )
        return role


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_email(self, value: str) -> str:
        return value.lower().strip()


class TokenSerializer(serializers.Serializer):
    """Single token payload (email verification or password reset)."""

    token = serializers.CharField()


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value: str) -> str:
        return value.lower().strip()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate_new_password(self, value: str) -> str:
        validate_password(value)
        return value


class ProfileUpdateSerializer(serializers.Serializer):
    """Updates allowed on the account itself once the email is verified."""

    full_name = serializers.CharField(required=False, allow_blank=True, max_length=150)

    def update(self, instance: User, validated_data: dict) -> User:
        if "full_name" in validated_data:
            instance.full_name = validated_data["full_name"]
            instance.save(update_fields=["full_name", "updated_at"])
        return instance
