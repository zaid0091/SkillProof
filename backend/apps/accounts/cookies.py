"""Refresh-token cookie handling for browser clients.

The access token stays in JavaScript memory; the refresh token is delivered as
an HttpOnly cookie so client code can never read it (docs/sacs.md section 3.4).
The cookie is scoped to the whole origin path because the optimistic frontend
guard (Next.js proxy) also inspects its presence before page requests.

``secure`` follows DEBUG: production settings run with DEBUG=False and serve
HTTPS only. SameSite=Lax blocks cross-site sends while allowing the frontend
(origin ``http://localhost:3000`` in development) to call the API on the same
site.
"""

from __future__ import annotations

from datetime import timedelta

from django.conf import settings
from django.http import HttpResponse

REFRESH_COOKIE_NAME = "sp_refresh"
REFRESH_COOKIE_PATH = "/"


def refresh_cookie_max_age() -> int:
    lifetime = settings.SIMPLE_JWT.get("REFRESH_TOKEN_LIFETIME", timedelta(days=7))
    return int(lifetime.total_seconds())


def set_refresh_cookie(response: HttpResponse, raw_token: str) -> None:
    response.set_cookie(
        REFRESH_COOKIE_NAME,
        raw_token,
        max_age=refresh_cookie_max_age(),
        path=REFRESH_COOKIE_PATH,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="Lax",
    )


def clear_refresh_cookie(response: HttpResponse) -> None:
    # delete_cookie() only accepts path/domain/samesite; the deletion cookie is
    # otherwise re-issued with matching attributes so browsers actually drop it.
    response.delete_cookie(
        REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
        samesite="Lax",
    )
