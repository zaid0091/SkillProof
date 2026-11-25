"""Celery application is loaded when the Django project is imported.

This guarantees that shared_task decorators bind to the same application the
worker starts with (`celery -A config worker`).
"""

from __future__ import annotations

from config.celery import app as celery_app

__all__ = ("celery_app",)
