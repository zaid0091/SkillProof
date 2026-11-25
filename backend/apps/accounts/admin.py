"""Django admin for accounts.

The admin is an internal operations tool. Product permissions are still enforced
through the API; admin access requires is_staff.
"""

from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import EmailVerificationToken, PasswordResetToken, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("-date_joined",)
    list_display = ("email", "full_name", "role", "is_verified", "is_active", "date_joined")
    list_filter = ("role", "is_verified", "is_active", "is_staff")
    search_fields = ("email", "full_name")
    readonly_fields = ("id", "date_joined", "created_at", "updated_at", "last_login")

    fieldsets = (
        (None, {"fields": ("id", "email", "password")}),
        ("Profile", {"fields": ("full_name", "role")}),
        (
            "Status",
            {
                "fields": (
                    "is_active",
                    "is_verified",
                    "is_staff",
                    "is_superuser",
                    "last_login",
                )
            },
        ),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
        ("Timestamps", {"fields": ("date_joined", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "full_name", "role", "password1", "password2"),
            },
        ),
    )


class OneTimeTokenAdmin(admin.ModelAdmin):
    """Read-only view of issued tokens: the raw value is never recoverable."""

    list_display = ("created_at", "user", "expires_at", "used_at")
    list_filter = ("used_at",)
    search_fields = ("user__email",)
    readonly_fields = (
        "id",
        "user",
        "token_hash",
        "expires_at",
        "used_at",
        "created_at",
        "updated_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(OneTimeTokenAdmin):
    pass


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(OneTimeTokenAdmin):
    pass
