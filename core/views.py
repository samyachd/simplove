from django.shortcuts import render


def core(request):
    profile = (
        getattr(request.user, "profile", None)
        if request.user.is_authenticated
        else None
    )
    return render(request, "index.html", {"profile": profile})
