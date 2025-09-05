from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login

def register(request):
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
    return render(request, "accounts/register.html", {"form": form})

def login(request):
    if request.method == "POST":
        if 

def logout(logout):


def delete_account(delete_account):


