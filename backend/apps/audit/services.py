"""Audit recording API.

Other modules record events through :func:`record` instead of writing to the
audit tables directly; the log's schema stays owned by this module
(docs/tad.md section 5.2).
"""

from __future__ import annotations

import logging

from apps.audit.models import AuditEvent

logger = logging.getLogger("skillproof.audit")


def record(
    event: str,
    *,
    actor=None,
    target: str = "",
    outcome: str = AuditEvent.Outcome.SUCCESS,
    metadata: dict | None = None,
) -> None:
    """Append one audit event.

    Never raises: an audit failure must not break the request that is being
    audited. Failures are logged loudly so operators can react.
    """
    try:
        AuditEvent.objects.create(
            event=event,
            outcome=outcome,
            actor=actor if getattr(actor, "pk", None) else None,
            actor_email=getattr(actor, "email", "") or target,
            target=target,
            metadata=metadata or {},
        )
    except Exception:  # pragma: no cover - depends on database failure
        logger.exception("Failed to record audit event %s", event)
