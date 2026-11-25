"""Account endpoints.

Phase 2 (SP-005 to SP-009) delivers registration, email verification, login,
refresh, logout, and password recovery.

    POST /api/v1/auth/register/
    POST /api/v1/auth/verify-email/
    POST /api/v1/auth/resend-verification/
    POST /api/v1/auth/login/
    POST /api/v1/auth/token/refresh/
    POST /api/v1/auth/logout/
    GET  /api/v1/auth/me/
    PATCH /api/v1/auth/me/
    POST /api/v1/auth/password-reset/
    POST /api/v1/auth/password-reset/confirm/
"""

from __future__ import annotations

from django.urls import path

from apps.accounts import views

app_name = "accounts"

urlpatterns = [
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/verify-email/", views.VerifyEmailView.as_view(), name="verify-email"),
    path(
        "auth/resend-verification/",
        views.ResendVerificationView.as_view(),
        name="resend-verification",
    ),
    path("auth/login/", views.LoginView.as_view(), name="login"),
    path("auth/token/refresh/", views.RefreshView.as_view(), name="token-refresh"),
    path("auth/logout/", views.LogoutView.as_view(), name="logout"),
    path("auth/me/", views.MeView.as_view(), name="me"),
    path("auth/password-reset/", views.PasswordResetRequestView.as_view(), name="password-reset"),
    path(
        "auth/password-reset/confirm/",
        views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
]
