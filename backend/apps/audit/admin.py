"""Django admin for the audit log.

Read-only by design: audit records are immutable (docs/sacs.md section 9.3),
so the admin exposes no add, change, or delete actions.
"""

from __future__ import annotations

from django.contrib import admin

from apps.audit.models import AuditEvent


@admin.register(AuditEvent)
class AuditEventAdmin(admin.ModelAdmin):
    list_display = ("created_at", "event", "outcome", "actor_email", "target")
    list_filter = ("event", "outcome")
    search_fields = ("actor_email", "target")
    readonly_fields = (
        "id",
        "event",
        "outcome",
        "actor",
        "actor_email",
        "target",
        "metadata",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
