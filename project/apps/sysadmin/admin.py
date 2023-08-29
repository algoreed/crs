from django.contrib import admin
from django.http import HttpResponseForbidden
from django.contrib.admin import AdminSite


def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You don't have permission to access this page")

    return _wrapped_view


class SuperUserAdminSite(AdminSite):
    def admin_view(self, view, cacheable=False):
        inner_view = super().admin_view(view, cacheable=cacheable)
        return superuser_required(inner_view)


# Register your models here.
