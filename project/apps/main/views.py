from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import District, LocalLevelGovernment, TrustRegion, Village, TrustVillage


# Create your views here.


def get_villages_by_llg_view(request):
    llg_id = request.GET.get("llg_id")
    villages = Village.objects.filter(llg_id=llg_id).values("id", "name")
    return JsonResponse(list(villages), safe=False)


def get_trust_villages_by_llg_view(request):
    llg_id = request.GET.get("llg_id")
    villages = TrustVillage.objects.filter(llg_id=llg_id).values("id", "name")
    return JsonResponse(list(villages), safe=False)


def get_trust_villages_by_district_view(request):
    district_id = request.GET.get("district_id")
    villages = TrustVillage.objects.filter(district_id=district_id).values("id", "name")
    return JsonResponse(list(villages), safe=False)


def get_villages_by_district_view(request):
    district_id = request.GET.get("district_id")
    villages = Village.objects.filter(district_id=district_id).values("id", "name")
    return JsonResponse(list(villages), safe=False)


def get_llgs_by_district_view(request):
    district_id = request.GET.get("district_id")
    llgs = LocalLevelGovernment.objects.filter(district_id=district_id).values(
        "id", "name"
    )
    return JsonResponse(list(llgs), safe=False)


def get_districts_by_province_view(request):
    province_id = request.GET.get("province_id")
    districts = District.objects.filter(province_id=province_id).values("id", "name")
    return JsonResponse(list(districts), safe=False)


def get_trust_regions_view(request):
    regions = TrustRegion.objects.all()
    return JsonResponse(list(regions), safe=False)


@login_required(login_url="login")
def home(request):
    return redirect("crs:index")
    # return custom_admin_site.index(request)


def customLoginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("crs:index")
        # Else, you can show an error message or something similar.
    return render(request, "registration/login.html", {"form": AuthenticationForm()})


def customLogoutView(request):
    logout(request)
    # return redirect("home")
    return render(request, "registration/logged_out.html", {})
