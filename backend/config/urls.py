"""Root URL configuration.

Everything the frontend consumes is versioned under /api/v1/. The Django admin
is available for internal operations only; all product behaviour is exposed
through the API so that permissions are enforced in one place.
"""

from __future__ import annotations

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("common.urls")),
    path("api/v1/", include("apps.accounts.urls")),
]
