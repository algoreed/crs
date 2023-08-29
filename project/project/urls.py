from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from apps.sysadmin.views import (
    customLoginView,
    customLogoutView,
    customSignupView,
    CustomPasswordResetView,
    passwordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCommpleteView,
)
from apps.community_context.views import DwellingAutocomplete

# from sysadmin.admin import SuperUserAdminSite


# default_admin_site = SuperUserAdminSite(name="admin")

urlpatterns = [
    path("admin/login/", customLoginView, name="admin:login"),
    path("crs/login/", customLoginView, name="crs:login"),
    path("logout/", customLogoutView, name="logout"),
    path("signup/", customSignupView, name="signup"),
    path(
        "password-reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        passwordResetDoneView,
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        PasswordResetCommpleteView.as_view(),
        name="password_reset_complete",
    ),
    path(
        "dwelling-autocomplete",
        DwellingAutocomplete.as_view(),
        name="dwelling_autocomplete",
    ),
    path("admin/", admin.site.urls),
    path("", include("apps.main.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)

# Configure Admin Titles
admin.site.site_header = "CRS Site Administration"
admin.site.site_title = "Admin Area"
admin.site.index_title = "CRS Site Administration"
