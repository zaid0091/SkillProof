"""Liveness and readiness endpoints.

Liveness must never touch a dependency: an orchestrator restarting the API
because PostgreSQL is briefly unavailable makes an outage worse. Readiness is
the opposite — it must reflect whether the instance can actually serve traffic.
"""

from __future__ import annotations

import logging

from django.core.cache import cache
from django.db import connection
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger("skillproof.health")

SERVICE = "skillproof-api"


def _database_ok() -> bool:
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return True
    except Exception:  # pragma: no cover - depends on infrastructure failure
        logger.exception("Readiness check failed: database unavailable")
        return False


def _cache_ok() -> bool:
    try:
        cache.set("health:probe", "ok", timeout=5)
        return cache.get("health:probe") == "ok"
    except Exception:  # pragma: no cover - depends on infrastructure failure
        logger.exception("Readiness check failed: cache unavailable")
        return False


class HealthView(APIView):
    """Process liveness."""

    authentication_classes: list = []
    permission_classes = [AllowAny]
    throttle_classes: list = []

    def get(self, request):
        return Response({"status": "ok", "service": SERVICE})


class ReadinessView(APIView):
    """Dependency readiness: database and cache."""

    authentication_classes: list = []
    permission_classes = [AllowAny]
    throttle_classes: list = []

    def get(self, request):
        checks = {"database": _database_ok(), "cache": _cache_ok()}
        ready = all(checks.values())
        return Response(
            {
                "status": "ready" if ready else "unavailable",
                "service": SERVICE,
                "checks": checks,
            },
            status=status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE,
        )
