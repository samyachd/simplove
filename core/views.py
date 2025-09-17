from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from profiles.models import MemberProfile
from users.models import UserAccount
from django.conf import settings
from utils.supabase_client import get_supabase
import mimetypes


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


def media_proxy(request, path):
    """Sert le fichier stocké dans Supabase via Django."""
    try:
        res = get_supabase().storage.from_(settings.SUPABASE_BUCKET).download(path)
    except Exception:
        raise Http404("Fichier introuvable")

    mime, _ = mimetypes.guess_type(path)
    return HttpResponse(res, content_type=mime or "application/octet-stream")
