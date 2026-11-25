# Isolated evaluation sandbox (Phase 5).
#
# This image is intentionally minimal: it has no database drivers, no Redis
# client, no application secrets, and no network access when started by
# docker-compose (network_mode: none). The API hands it a job manifest through a
# bind mount; the worker writes a result manifest back and then exits.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Only the tools required to execute and analyse Python submissions.
RUN pip install --no-cache-dir \
    pytest==8.* \
    pytest-cov==6.* \
    radon==6.* \
    ruff==0.9.*

RUN useradd --create-home --uid 1001 sandbox \
    && mkdir -p /work \
    && chown -R sandbox:sandbox /work

WORKDIR /work
USER sandbox

ENTRYPOINT ["python", "/opt/sandbox/runner.py"]
