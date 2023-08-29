from django.urls import path
from django.shortcuts import redirect
from . import views
from .admin import custom_admin_site


def redirect_to_customadmin(request):
    # If user is not authenticated and path contains "/admin", redirect to "admin/login"

    if not request.user.is_authenticated and "/admin" in request.path:
        return redirect("admin:login")

    elif request.user.is_authenticated and "/admin" in request.path:
        return redirect("admin:index")
    # If user is not authenticated and path does not contain "/admin", redirect to "crs/login"

    elif not request.user.is_authenticated:
        return redirect("crs:login")
    return redirect("/crs/")


urlpatterns = [
    path("", redirect_to_customadmin),
    path(
        "get_districts_by_province/",
        views.get_districts_by_province_view,
        name="get_districts_by_province",
    ),
    path(
        "get_llgs_by_district/",
        views.get_llgs_by_district_view,
        name="get_llgs_by_district",
    ),
    path(
        "get_villages_by_district/",
        views.get_villages_by_district_view,
        name="get_villages_by_district",
    ),
    path(
        "get_trust_villages_by_district/",
        views.get_trust_villages_by_district_view,
        name="get_trust_villages_by_district",
    ),
    path(
        "get_villages_by_llg/",
        views.get_villages_by_llg_view,
        name="get_villages_by_llg",
    ),
    path(
        "get_trust_villages_by_llg/",
        views.get_trust_villages_by_llg_view,
        name="get_trust_villages_by_llg",
    ),
    path("get_trust_regions/", views.get_trust_regions_view, name="get_trust_regions"),
    # path("login/", views.customLoginView, name="login"),
    # path("logout/", views.customLogoutView, name="logout"),
    path("crs/", custom_admin_site.urls),
]
