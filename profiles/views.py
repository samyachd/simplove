from django.shortcuts import render, redirect, get_object_or_404
from profiles.decorators import profile_required
from .models import MemberProfile
from .forms import MemberProfileForm, ProfileFilterForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileFilterForm


@login_required
@profile_required
def profile_view(request):
    """Affiche le profil de l'utilisateur connecté"""
    profile, created = MemberProfile.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"user": request.user, "profile": profile})


@login_required
@profile_required
def profile_edit(request, pk):
    """Modification du profil"""
    profile, created = MemberProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = MemberProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profiles:profile")
    else:
        form = MemberProfileForm(instance=profile)

    return render(request, "profile_edit.html", {"form": form})


@login_required
@profile_required
def profile_detail(request, pk):
    profile = get_object_or_404(MemberProfile, pk=pk, user__is_active=True)
    return render(request, "profile_detail.html", {"profile": profile})


@login_required
def create_profile(request):
    profile, created = MemberProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = MemberProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("core:core")
    else:

        form = MemberProfileForm(instance=profile)
    context = {"form": form} | {"hide_navbar": True}
    return render(request, "create_profile.html", context)


@login_required
def profile_list(request):
    form = ProfileFilterForm(request.GET or None)
    profiles = MemberProfile.objects.filter(
        user__is_superuser=False, user__is_active=True
    ).exclude(user=request.user)

    if form.is_valid():
        q = form.cleaned_data.get("q")
        age_min = form.cleaned_data.get("age_min")
        age_max = form.cleaned_data.get("age_max")
        gender = form.cleaned_data.get("gender")
        orientation = form.cleaned_data.get("orientation")
        location = form.cleaned_data.get("location")
        looking_for = form.cleaned_data.get("looking_for")
        interests = form.cleaned_data.get("interests")

        if q:
            profiles = profiles.filter(user__username__icontains=q)
        if age_min:
            profiles = profiles.filter(age__gte=age_min)
        if age_max:
            profiles = profiles.filter(age__lte=age_max)
        if gender:
            profiles = profiles.filter(gender=gender)
        if orientation:
            profiles = profiles.filter(orientation=orientation)
        if location:
            profiles = profiles.filter(location__icontains=location)
        if looking_for:
            profiles = profiles.filter(looking_for=looking_for)
        if interests:
            for interest in [i.strip() for i in interests.split(",") if i.strip()]:
                profiles = profiles.filter(interest__icontains=interest)

    return render(request, "profile_list.html", {"profiles": profiles, "form": form})
