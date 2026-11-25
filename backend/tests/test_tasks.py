"""Celery task registration and round-trip behaviour.

In tests the broker is eager, so this proves the task is importable and returns
a result without requiring Redis. The real Redis round-trip is exercised by
scripts/celery_ping.py against the dev stack.
"""

from __future__ import annotations

from common.tasks import ping


def test_ping_task_is_registered_and_returns_pong():
    result = ping.delay("contract-test")

    payload = result.get(timeout=5)

    assert payload["status"] == "pong"
    assert payload["payload"] == "contract-test"
    assert payload["worker"]
    assert payload["at"] > 0
