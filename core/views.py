from django.http import HttpResponse
from django.shortcuts import render, redirect
from profiles.models import MemberProfile
from users.models import UserAccount

def core(request):
    if (
        request.user.is_authenticated
        and UserAccount.objects.get(user=request.user).phone_number == ""
    ):
        return redirect("users:create_account")
    elif (
        request.user.is_authenticated
        and MemberProfile.objects.get(user=request.user).looking_for == ""
    ):
        return redirect("profiles:create_profile")
    return render(request, "index.html")
