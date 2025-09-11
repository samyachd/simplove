from django.shortcuts import render, redirect
from profiles.models import MemberProfile


def core(request):
    if request.user.is_authenticated and MemberProfile.objects.get(user=request.user).looking_for is "":
        return redirect("profiles:create_profile")
    return render(request, "index.html")