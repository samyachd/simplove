from .forms import RegisterForm
from profiles.forms import MemberProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from profiles.models import MemberProfile
from django.shortcuts import render, redirect, get_object_or_404

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            return render(request, )
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


def account_view(request):
    if not request.user.is_authenticated:
        return render(request, "registration/login_error.html")
    else:
        return render(request, "registration/account.html", {"User": User.username})
    
def post_register_profile(request):
    if request.method == "POST":
        form = MemberProfileForm(request.POST)
        if form.is_valid():
            profile = MemberProfile.objects.create(
                gender = form.cleaned_data["gender"],
                orientation = form.cleaned_data["orientation"],
                age = form.cleaned_data["age"],
                bio = form.cleaned_data["bio"],
                location = form.cleaned_data["location"],
                interest = form.cleaned_data["interest"],
                looking_for = form.cleaned_data["looking_for"],
            )

      

