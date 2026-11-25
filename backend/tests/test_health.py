"""Health endpoint tests cover the Phase 1 infrastructure exit criteria."""

from __future__ import annotations

import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_liveness_does_not_require_authentication():
    response = APIClient().get("/api/v1/health/")

    assert response.status_code == 200
    assert response.data["status"] == "ok"
    assert response.data["service"] == "skillproof-api"


def test_readiness_reports_dependencies():
    response = APIClient().get("/api/v1/health/ready/")

    assert response.status_code == 200
    assert response.data["status"] == "ready"
    assert response.data["checks"] == {"database": True, "cache": True}


def test_health_endpoints_are_versioned():
    response = APIClient().get("/api/v1/health/")

    assert response["Content-Type"].startswith("application/json")
