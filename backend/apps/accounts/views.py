"""Account API views.

Endpoint contract (docs/tad.md section 11.2):

    POST   /api/v1/auth/register/                 create account + send verification link
    POST   /api/v1/auth/verify-email/              consume a verification token
    POST   /api/v1/auth/resend-verification/       reissue a verification link (authenticated)
    POST   /api/v1/auth/login/                     exchange credentials for tokens
    POST   /api/v1/auth/token/refresh/             rotate the refresh token, mint an access token
    POST   /api/v1/auth/logout/                    revoke the presented refresh token
    GET    /api/v1/auth/me/                        current account
    PATCH  /api/v1/auth/me/                        update account (verified users only)
    POST   /api/v1/auth/password-reset/            request a reset link (never discloses existence)
    POST   /api/v1/auth/password-reset/confirm/    consume a reset token and set a new password

Browser token handling: the access token is returned in the body for in-memory
storage; the refresh token is set as an HttpOnly cookie and rotated on every
use. Cookie-based endpoints additionally verify the request origin
(docs/sacs.md sections 3.4 and 6.5).
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts import services
from apps.accounts.cookies import (
    REFRESH_COOKIE_NAME,
    clear_refresh_cookie,
    set_refresh_cookie,
)
from apps.accounts.models import User
from apps.accounts.serializers import (
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    TokenSerializer,
    UserSerializer,
)
from apps.audit import services as audit_services
from apps.audit.models import AuditEvent
from common.exceptions import ApiError, envelope
from common.permissions import IsVerifiedUser
from common.security import request_origin_is_trusted


class RegisterView(APIView):
    """Public registration. Privileged roles can never be supplied by clients."""

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.register_user(**serializer.validated_data)
        return Response(
            {
                "user": UserSerializer(user).data,
                "detail": "Account created. Check your email to verify your address.",
            },
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(APIView):
    """Consume a single-use verification token."""

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = services.verify_email(serializer.validated_data["token"])
        return Response({"user": UserSerializer(user).data, "detail": "Email address verified."})


class ResendVerificationView(APIView):
    """Reissue the verification link for the authenticated account."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        services.resend_verification(request.user)
        return Response({"detail": "Verification email sent."})


class LoginView(APIView):
    """Exchange credentials for an access token and a refresh cookie."""

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, access, refresh = services.login(**serializer.validated_data)
        response = Response({"access": access, "user": UserSerializer(user).data})
        set_refresh_cookie(response, refresh)
        return response


class RefreshView(APIView):
    """Rotate the refresh token and mint a new access token."""

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request):
        raw_token = request.COOKIES.get(REFRESH_COOKIE_NAME) or request.data.get("refresh")
        from_cookie = REFRESH_COOKIE_NAME in request.COOKIES

        if not raw_token:
            raise ApiError("not_authenticated", "No session to refresh.", status_code=401)

        if from_cookie and not request_origin_is_trusted(request):
            audit_services.record(
                AuditEvent.Event.TOKEN_REFRESH_FAILED,
                outcome=AuditEvent.Outcome.FAILURE,
                metadata={"reason": "untrusted_origin"},
            )
            raise ApiError("permission_denied", "Request origin is not allowed.", status_code=403)

        try:
            user = User.objects.get(pk=self._user_id(raw_token), is_active=True)
        except (TokenError, User.DoesNotExist, KeyError, ValueError, TypeError, ValidationError):
            audit_services.record(
                AuditEvent.Event.TOKEN_REFRESH_FAILED,
                outcome=AuditEvent.Outcome.FAILURE,
                metadata={"reason": "invalid_token"},
            )
            response = Response(
                envelope(
                    "invalid_refresh_token",
                    "Your session has expired. Please sign in again.",
                ),
                status=status.HTTP_401_UNAUTHORIZED,
            )
            clear_refresh_cookie(response)
            return response

        # Rotation: the presented token is revoked and replaced.
        services.blacklist_refresh_token(raw_token)
        access, refresh = services.issue_tokens(user)
        response = Response({"access": access, "user": UserSerializer(user).data})
        set_refresh_cookie(response, refresh)
        return response

    @staticmethod
    def _user_id(raw_token: str):
        return RefreshToken(raw_token).payload.get("user_id")


class LogoutView(APIView):
    """Revoke the presented refresh token and clear the session cookie."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        raw_token = request.COOKIES.get(REFRESH_COOKIE_NAME) or request.data.get("refresh")
        if raw_token:
            services.blacklist_refresh_token(raw_token)
        audit_services.record(
            AuditEvent.Event.LOGOUT, actor=request.user, target=request.user.email
        )
        response = Response({"detail": "Signed out."})
        clear_refresh_cookie(response)
        return response


class MeView(APIView):
    """Current account. Reads are allowed unverified; writes require verification."""

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsAuthenticated(), IsVerifiedUser()]
        return super().get_permissions()

    def get(self, request):
        return Response({"user": UserSerializer(request.user).data})

    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.update(request.user, serializer.validated_data)
        return Response({"user": UserSerializer(user).data})


class PasswordResetRequestView(APIView):
    """Start recovery. The response is identical for known and unknown emails."""

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.request_password_reset(serializer.validated_data["email"])
        return Response(
            {"detail": "If an account exists for that address, a reset link has been sent."}
        )


class PasswordResetConfirmView(APIView):
    """Consume a reset token, set the new password, and sign out all sessions."""

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.confirm_password_reset(
            raw_token=serializer.validated_data["token"],
            new_password=serializer.validated_data["new_password"],
        )
        response = Response(
            {"detail": "Password updated. All other sessions have been signed out."}
        )
        clear_refresh_cookie(response)
        return response
