"""InstaShare API URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)

from apps.accounts import views as accounts_views
from apps.files import views as files_views
from apps.core import views as core_views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"users", accounts_views.UserViewSet, basename="user")
router.register(r"files", files_views.FileViewSet, basename="file")

urlpatterns = [
    path("", core_views.IndexView.as_view()),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/login/", accounts_views.TokenView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "openapi",
        get_schema_view(
            title="Drones API",
            description="Drone Infrastructure API",
            version="1.0.0",
            url="https://drones-api.ragnarok22.dev/",
        ),
        name="openapi-schema",
    ),
    path("docs/", core_views.DocsView.as_view(), name="docs"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
