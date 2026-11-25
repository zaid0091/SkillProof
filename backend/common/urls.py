"""URLs for infrastructure endpoints, mounted under /api/v1/."""

from __future__ import annotations

from django.urls import path

from common import health

app_name = "common"

urlpatterns = [
    path("health/", health.HealthView.as_view(), name="health"),
    path("health/ready/", health.ReadinessView.as_view(), name="health-ready"),
]
