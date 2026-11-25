"""Consistent API error responses.

Every failure returns the same envelope so the frontend has one shape to handle:

    {
      "error": {
        "code": "validation_error",
        "message": "Request validation failed.",
        "details": {"email": ["Enter a valid email address."]}
      }
    }

Django/DRF defaults leak field names inconsistently across endpoints; this
handler is the single place that normalises them. Internal details, secrets, and
stack traces are never included.
"""

from __future__ import annotations

import logging
from typing import Any

from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.http import Http404
from rest_framework import exceptions as drf_exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("skillproof.api")


class ApiError(Exception):
    """Raised by domain code for an expected, client-facing failure.

    Example:
        raise ApiError("assessment_not_published", "This assessment is not available.", status_code=409)
    """

    def __init__(
        self,
        code: str,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details


def envelope(code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    """Build the standard error body."""
    body: dict[str, Any] = {"code": code, "message": message}
    if details not in (None, {}, []):
        body["details"] = details
    return {"error": body}


def _first_code(detail: Any) -> str | None:
    """Extract the DRF error code from nested detail structures."""
    if isinstance(detail, dict):
        for value in detail.values():
            found = _first_code(value)
            if found:
                return found
        return None
    if isinstance(detail, (list, tuple)):
        for value in detail:
            found = _first_code(value)
            if found:
                return found
        return None
    return getattr(detail, "code", None)


def _humanise(code: str) -> str:
    return code.replace("_", " ").strip().capitalize()


def api_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """DRF EXCEPTION_HANDLER implementation."""
    if isinstance(exc, ApiError):
        return Response(
            envelope(exc.code, exc.message, exc.details),
            status=exc.status_code,
        )

    if isinstance(exc, (Http404, DjangoValidationError, DjangoPermissionDenied)):
        converted = drf_exceptions.ValidationError(
            getattr(exc, "message_dict", None) or getattr(exc, "messages", [str(exc)])
        )
        exc = converted

    response = drf_exception_handler(exc, context)
    if response is None:
        # Unhandled exception: log for operators, return an opaque 500 to clients.
        logger.exception("Unhandled API exception", exc_info=exc)
        return Response(
            envelope("server_error", "An unexpected error occurred."),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    code = _first_code(response.data) or "error"
    detail = response.data

    if isinstance(exc, drf_exceptions.ValidationError):
        code = "validation_error"
        message = "Request validation failed."
        details = detail
    elif isinstance(exc, drf_exceptions.NotAuthenticated):
        code = "not_authenticated"
        message = "Authentication credentials were not provided or are invalid."
        details = None
    elif isinstance(exc, drf_exceptions.AuthenticationFailed):
        code = "authentication_failed"
        message = "Authentication failed."
        details = None
    elif isinstance(exc, drf_exceptions.PermissionDenied):
        code = "permission_denied"
        message = "You do not have permission to perform this action."
        details = None
    elif isinstance(exc, drf_exceptions.Throttled):
        code = "throttled"
        message = "Too many requests. Try again later."
        details = {"retry_after": exc.wait}
    elif isinstance(exc, drf_exceptions.NotFound):
        code = "not_found"
        message = "The requested resource was not found."
        details = None
    elif isinstance(exc, drf_exceptions.MethodNotAllowed):
        code = "method_not_allowed"
        message = "This method is not allowed for the requested resource."
        details = None
    elif isinstance(exc, drf_exceptions.UnsupportedMediaType):
        code = "unsupported_media_type"
        message = "The request content type is not supported."
        details = None
    else:
        message = _humanise(code) + "."

    return Response(
        envelope(code, message, details),
        status=response.status_code,
        headers=getattr(response, "headers", None),
    )
