from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from profiles.models import MemberProfile
from profiles.decorators import profile_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )

            MemberProfile.objects.create(user=user)

            login(request, user)
            return redirect("profiles:create_profile")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
@profile_required
def account_view(request):
    if not request.user.is_authenticated:
        return render(request, "registration/login_error.html")
    else:
        return render(request, "registration/account.html", {"User": request.user})




