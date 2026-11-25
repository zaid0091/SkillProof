"""Celery application factory.

Only infrastructure work belongs on this queue: assessment execution scheduling,
code analysis, GitHub synchronisation, report generation, and notifications.
Untrusted student code never runs here — it runs in the isolated evaluation
sandbox described in docs/tad.md section 7.
"""

from __future__ import annotations

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("skillproof")

# All Celery configuration lives in Django settings under the CELERY_ prefix so
# that environments (dev/prod/test) are configured in one place.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Discover tasks.py modules inside every installed app.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self) -> str:  # pragma: no cover - manual diagnostic helper
    """Print the current request for `celery inspect` troubleshooting."""
    print(f"Request: {self.request!r}")
    return "ok"
