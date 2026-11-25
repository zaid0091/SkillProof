"""Development settings: verbose errors, permissive hosts, console email."""

from __future__ import annotations

from .base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "[::1]"]

# Local development cannot resolve Docker service names, so SQLite is used
# unless DATABASE_URL is set explicitly (docker-compose sets PostgreSQL).
# Nothing else in this module widens security settings for non-dev use.

INTERNAL_IPS = ["127.0.0.1"]

LOGGING["root"]["level"] = "DEBUG"  # noqa: F405
LOGGING["loggers"]["django.db.backends"] = {  # noqa: F405
    "handlers": ["console"],
    "level": "WARNING",
    "propagate": False,
}

# CORS for the local Next.js dev server, including common alternate ports.
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CSRF_TRUSTED_ORIGINS = list(CORS_ALLOWED_ORIGINS)
