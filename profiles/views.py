from django.shortcuts import render, redirect
from .forms import MemberProfilForm
from django.contrib.auth.decorators import login_required


@login_required
def profile_edit(request):
    profile = request.user.profile
    if request.method == "POST":
        form = MemberProfilForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profiles:detail", profile.id)
    else:
        form = MemberProfilForm(instance=profile)
    return render(request, "profiles/profile_edit.html", {"form": form})
