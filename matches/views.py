from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from .models import Match
from .models import Evaluation, Match

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

@login_required
def like_user(request, user_id):
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")
    target = get_object_or_404(User, id=user_id)
    if target == request.user:
        messages.error(request, "You cannot like yourself.")
        return redirect("browse_profiles")
    obj, _ = Evaluation.objects.get_or_create(
        evaluator=request.user, target=target, defaults={"status": Evaluation.LIKE}
    )
    if obj.status != Evaluation.LIKE:
        obj.status = Evaluation.LIKE
        obj.save()
    _ensure_match_state(request.user, target)
    messages.success(request, f"You liked @{target.username}.")
    return redirect("my_matches")

@login_required
def pass_user(request, user_id):
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
    messages.info(request, f"You passed on @{target.username}.")
    return redirect("browse_profiles")

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
    return redirect("my_matches")


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


@login_required
def browse_profiles(request):
    """Super basic browse page: show everyone except me."""
    evaluated_ids = Evaluation.objects.filter(evaluator=request.user).values_list(
        "target_id", flat=True
    )
    users = User.objects.exclude(id=request.user.id).exclude(id__in=evaluated_ids)[:20]
    return render(request, "browse.html", {"users": users})
