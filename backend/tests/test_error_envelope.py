"""The API error envelope is a contract the frontend depends on (FIS section 14)."""

from __future__ import annotations

from rest_framework import exceptions as drf_exceptions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from common.exceptions import ApiError, envelope


class ApiErrorView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]

    def get(self, request):
        raise ApiError(
            "assessment_not_published",
            "This assessment is not available.",
            status_code=409,
        )


class ValidationView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]

    def get(self, request):
        raise drf_exceptions.ValidationError({"email": ["Enter a valid email address."]})


class PermissionView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]

    def get(self, request):
        raise drf_exceptions.PermissionDenied()


class OkView(APIView):
    authentication_classes: list = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


def test_domain_error_uses_envelope():
    response = ApiErrorView.as_view()(APIRequestFactory().get("/"))

    assert response.status_code == 409
    assert response.data == {
        "error": {
            "code": "assessment_not_published",
            "message": "This assessment is not available.",
        }
    }


def test_validation_error_exposes_field_details():
    response = ValidationView.as_view()(APIRequestFactory().get("/"))

    assert response.status_code == 400
    body = response.data["error"]
    assert body["code"] == "validation_error"
    assert body["message"] == "Request validation failed."
    assert body["details"] == {"email": ["Enter a valid email address."]}


def test_permission_denied_does_not_leak_internals():
    response = PermissionView.as_view()(APIRequestFactory().get("/"))

    assert response.status_code == 403
    assert response.data["error"]["code"] == "permission_denied"
    assert response.data["error"]["message"] == (
        "You do not have permission to perform this action."
    )


def test_envelope_omits_empty_details():
    assert envelope("not_found", "Missing.") == {
        "error": {"code": "not_found", "message": "Missing."}
    }
