"""Sandbox entrypoint for isolated evaluation (Phase 5).

Contract
--------
1. The API writes ``/work/job.json`` containing only what is required to run
   the submission: source files, the test command, and resource limits.
2. This process executes the job inside the container's restricted filesystem
   (read-only root, writable /work tmpfs, no network, non-root user).
3. A machine-readable ``/work/result.json`` is written with test outcomes and
   tool findings. Nothing else is persisted.

Phase 1 only defines the contract and the failure modes. Test execution,
static analysis integration, and result normalisation are implemented in
Phase 5 (SP-019 to SP-021).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

JOB_PATH = Path("/work/job.json")
RESULT_PATH = Path("/work/result.json")

NOT_IMPLEMENTED = {
    "status": "failed",
    "reason": "sandbox_not_implemented",
    "detail": "Isolated evaluation is scheduled for Phase 5 (SP-019..SP-021).",
}


def main() -> int:
    if not JOB_PATH.exists():
        RESULT_PATH.write_text(json.dumps(NOT_IMPLEMENTED), encoding="utf-8")
        return 1

    # Deliberately fail closed: an unrecognised job must never be executed by a
    # partially implemented runner.
    RESULT_PATH.write_text(
        json.dumps(
            {
                **NOT_IMPLEMENTED,
                "detail": "Runner received a job manifest but has no executor yet.",
                "job_bytes": JOB_PATH.stat().st_size,
            }
        ),
        encoding="utf-8",
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
