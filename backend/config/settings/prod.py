"""Production settings.

Security controls are enabled here rather than in base so that local HTTP
development stays workable. Every value can be overridden by the deployment
environment, but the safe direction is the default.
"""

from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = False

# Reverse proxies and load balancers terminate TLS in front of the app.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False  # the SPA reads the CSRF token for unsafe requests
CSRF_COOKIE_SAMESITE = "Lax"

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])  # noqa: F405

if not SECRET_KEY or SECRET_KEY.startswith("insecure"):  # noqa: F405
    raise RuntimeError("DJANGO_SECRET_KEY must be set to a strong value in production.")
