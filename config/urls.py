"""InstaShare API URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

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
    path("api/logout/", accounts_views.LogoutView.as_view(), name="logout"),
    path("api/register/", accounts_views.RegistrationView.as_view(), name="register"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
