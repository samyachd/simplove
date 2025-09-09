from django.shortcuts import render, redirect, get_object_or_404
from .models import MemberProfile
from .forms import MemberProfileForm
from django.contrib.auth.decorators import login_required


@login_required
def profile_edit(request, pk):
    profile = get_object_or_404(MemberProfile, pk=pk)
    if request.method == "POST":
        form = MemberProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profiles:detail", profile.id)
    else:
        form = MemberProfileForm(instance=profile)
    return render(request, "profile_edit.html", {"form": form})


def profile_list(request):
    query = request.GET.get("q", "")
    if query:
        profiles = MemberProfile.objects.filter(user__username__icontains=query)
    else:
        profiles = MemberProfile.objects.all()
    return render(
        request, "profile_list.html", {"profiles": profiles, "query": query}
    )


def profile_detail(request, pk):
    profile = get_object_or_404(MemberProfile, pk=pk)
    return render(request, "profile_detail.html", {"profile": profile})
