from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from project.forms import SignupForm, PasswordResetForm, SetPasswordForm
from django.contrib import messages


# Create your views here.


def customLoginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                # Redirect based on the request path
                if "/admin" in request.path:
                    return redirect("admin:index")
                else:
                    return redirect("crs:index")
            else:
                messages.error(
                    request, "You don't have permission to access the admin site."
                )
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "registration/login.html", {"form": AuthenticationForm()})


def customLogoutView(request):
    logout(request)
    return render(request, "registration/logged_out.html")


def customSignupView(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect based on the request path
            if "/admin" in request.path:
                return redirect("admin:index")
            else:
                return redirect("crs:index")
    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})


class CustomPasswordResetView(auth_views.PasswordResetView):
    form_class = PasswordResetForm


def passwordResetDoneView(request):
    return render(request, "registration/password_reset_done.html")


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = SetPasswordForm
    template_name = "registration/password_reset_confirm.html"


class PasswordResetCommpleteView(auth_views.PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"
