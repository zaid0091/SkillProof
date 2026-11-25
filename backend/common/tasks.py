"""Infrastructure tasks.

This module is imported explicitly by config/celery.py so workers register the
tasks even though ``common`` is not a Django app.
"""

from __future__ import annotations

import platform
import socket
import time

from celery import shared_task


@shared_task(name="common.ping")
def ping(payload: str | None = None) -> dict[str, object]:
    """Round-trip probe used by the Phase 1 queue smoke test.

    Returns worker identity so operators can confirm which process executed the
    task, then compares it with the enqueueing host.
    """
    return {
        "status": "pong",
        "payload": payload,
        "worker": socket.gethostname(),
        "platform": platform.system(),
        "at": time.time(),
    }
