from django.shortcuts import render


def core(request):
    profile = getattr(request.user, "profile_or_none", None)
    return render(request, "index.html", {"profile": profile})
