"""GitHub Integration domain module."""

from __future__ import annotations

from django.apps import AppConfig


class GithubIntegrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.github_integration"
    label = "github_integration"
    verbose_name = "GitHub Integration"
