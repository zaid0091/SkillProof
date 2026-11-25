"""Request-level security helpers shared across modules."""

from __future__ import annotations

from django.conf import settings


def request_origin_is_trusted(request) -> bool:
    """CSRF defence for cookie-authenticated endpoints (docs/sacs.md section 6.5).

    Browsers always attach an ``Origin`` header to cross-site POSTs, so a
    mismatch with the configured trusted origins means a forged request.
    Requests without an ``Origin`` header come from non-browser clients (curl,
    tests, server-to-server) and cannot exploit a cookie-based CSRF vector.
    """
    origin = request.headers.get("Origin") or request.headers.get("Referer") or ""
    if not origin:
        return True
    trusted = set(settings.CSRF_TRUSTED_ORIGINS) | set(settings.CORS_ALLOWED_ORIGINS)
    trusted.add(settings.FRONTEND_URL)
    return origin in trusted
