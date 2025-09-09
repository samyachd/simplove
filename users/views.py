from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth import logout


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            login(request, user)
            return redirect("/")  # redirection après inscription
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def account_view(request):
    if not request.user.is_authenticated:
        return render(request, "registration/login_error.html")
    else:
        return render(request, "registration/account.html", {"User": User.username})


def logout_view(request):
    logout(request)
    return redirect("/")
