from django.contrib import messages
from django.contrib.auth.decorators import login_required
from profiles.decorators import profile_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from .models import Match
from .models import Evaluation, Match
import random

User = get_user_model()


def _ensure_match_state(a, b):
    a_likes_b = Evaluation.objects.filter(
        evaluator=a, target=b, status=Evaluation.LIKE
    ).exists()
    b_likes_a = Evaluation.objects.filter(
        evaluator=b, target=a, status=Evaluation.LIKE
    ).exists()
    if a_likes_b and b_likes_a:
        match, _ = Match.objects.get_or_create(
            **({"user1": a, "user2": b} if a.id < b.id else {"user1": b, "user2": a})
        )
        if not match.is_active:
            match.is_active = True
            match.save()
    else:
        Match.objects.filter(Match.pair_q(a, b), is_active=True).update(is_active=False)


@profile_required
@login_required
def like_user(request, user_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        return redirect("matches:browse_profiles")

    obj, _ = Evaluation.objects.get_or_create(
        evaluator=request.user, target=target, defaults={"status": Evaluation.LIKE}
    )
    obj.status = Evaluation.LIKE
    obj.save()
    _ensure_match_state(request.user, target)

    # Afficher le prochain profil
    evaluated_ids = Evaluation.objects.filter(evaluator=request.user).values_list(
        "target_id", flat=True
    )
    candidates = User.objects.exclude(id=request.user.id).exclude(id__in=evaluated_ids)
    next_user = random.choice(candidates) if candidates.exists() else None

    return render(request, "browse.html", {"user": next_user})


@profile_required
@login_required
def pass_user(request, user_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    target = get_object_or_404(User, id=user_id)
    obj, _ = Evaluation.objects.get_or_create(
        evaluator=request.user, target=target, defaults={"status": Evaluation.UNLIKE}
    )
    obj.status = Evaluation.UNLIKE
    obj.save()
    _ensure_match_state(request.user, target)

    # Afficher le prochain profil
    evaluated_ids = Evaluation.objects.filter(evaluator=request.user).values_list(
        "target_id", flat=True
    )
    candidates = User.objects.exclude(id=request.user.id).exclude(id__in=evaluated_ids)
    next_user = random.choice(candidates) if candidates.exists() else None

    return render(request, "browse.html", {"user": next_user})


@profile_required
@login_required
def remove_like(request, user_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    target = get_object_or_404(User, id=user_id)
    obj, _ = Evaluation.objects.get_or_create(
        evaluator=request.user, target=target, defaults={"status": Evaluation.UNLIKE}
    )
    if obj.status != Evaluation.UNLIKE:
        obj.status = Evaluation.UNLIKE
        obj.save()
    _ensure_match_state(request.user, target)
    messages.warning(request, f"You removed your like for @{target.username}.")
    return redirect("matches:my_matches")


@profile_required
@login_required
def my_matches(request):
    matches = Match.objects.filter(user1=request.user) | Match.objects.filter(
        user2=request.user
    )

    # Définir "other" pour chaque match
    for match in matches:
        if match.user1_id == request.user.id:
            match.other = match.user2
        else:
            match.other = match.user1

    return render(request, "matches_list.html", {"matches": matches})


@profile_required
@login_required
def browse_profiles(request):
    """Afficher un profil aléatoire que l'utilisateur n'a pas encore évalué."""
    evaluated_ids = Evaluation.objects.filter(evaluator=request.user).values_list(
        "target_id", flat=True
    )

    candidates = User.objects.exclude(id=request.user.id).exclude(id__in=evaluated_ids)

    if candidates.exists():
        user = random.choice(candidates)  # Choisir un profil au hasard
        return render(request, "browse.html", {"user": user})
    else:
        return render(request, "browse.html", {"user": None})


@login_required
def like(request, user_id):
    target = get_object_or_404(User, id=user_id)
    Evaluation.objects.create(evaluator=request.user, target=target, liked=True)
    return redirect("matches:browse_profiles")  # ← retour au profil suivant


@login_required
def pass_profile(request, user_id):
    target = get_object_or_404(User, id=user_id)
    Evaluation.objects.create(evaluator=request.user, target=target, liked=False)
    return redirect("matches:browse_profiles")  # ← retour au profil suivant
