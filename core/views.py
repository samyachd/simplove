from django.shortcuts import render
from django.http import HttpResponse


def core(request):
    profile = (
        getattr(request.user, "profile", None)
        if request.user.is_authenticated
        else None
    )
    return render(request, "index.html", {"profile": profile})


def home(request):
    return render(request, "core/index.html")


def core_view(request):
    return render(request, "core/index.html")


from django.shortcuts import render, redirect
from profiles.models import MemberProfile


def core(request):
    if (
        request.user.is_authenticated
        and MemberProfile.objects.get(user=request.user).looking_for is ""
    ):
        return redirect("profiles:create_profile")
    return render(request, "index.html")
