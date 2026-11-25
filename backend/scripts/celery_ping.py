"""Enqueue a Celery ping and wait for the worker's reply.

Proves the Phase 1 exit criterion that API -> Redis -> worker communication
works. Requires Redis and a running worker with config.settings.dev (or prod)
loaded:

    celery -A config worker -l info

Usage:
    python scripts/celery_ping.py
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django  # noqa: E402

django.setup()

from common.tasks import ping  # noqa: E402


def main() -> int:
    result = ping.delay("phase-1-smoke-test")
    print(f"queued task id: {result.id}")
    print("waiting up to 15s for a worker...")
    try:
        reply = result.get(timeout=15)
    except Exception as exc:  # timeout or broker error
        print(f"\nFAILED: {type(exc).__name__}: {exc}")
        print("Check that Redis is running and a Celery worker is started.")
        return 1

    print(json.dumps(reply, indent=2))
    print("\nOK: queue round-trip succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
