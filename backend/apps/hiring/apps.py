"""Hiring domain module."""

from __future__ import annotations

from django.apps import AppConfig


class HiringConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.hiring"
    label = "hiring"
    verbose_name = "Hiring"
