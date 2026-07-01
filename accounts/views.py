from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm


def splash_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "accounts/splash.html")

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, "accounts/login.html")


def register_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {
        "form": form
    })


def forgot_password(request):
    return render(request, "accounts/forgot_password.html")


def profile(request):
    return render(request, "accounts/profile.html")


def logout_view(request):
    logout(request)
    return redirect("login")
