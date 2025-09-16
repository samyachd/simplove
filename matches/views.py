from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model


from django.core.paginator import Paginator
from django.db.models import Q, Case, When, F, IntegerField, CharField
from .models import Match, Evaluation



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

    return redirect("matches:my_matches")

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

    return redirect("matches:browse_profiles")

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

@login_required
def browse_profiles(request):
    """Super basic browse page: show everyone except me."""
    evaluated_ids = Evaluation.objects.filter(evaluator=request.user).values_list(
        "target_id", flat=True
    )
    users = User.objects.exclude(id=request.user.id).exclude(id__in=evaluated_ids)[:20]
    return render(request, "browse.html", {"users": users})


# developpements

# matches/views.py
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Case, When, F, IntegerField, CharField
from django.shortcuts import render
from .models import Match, Evaluation

@login_required
def my_matches(request):
    user = request.user

    # Active matches that include me, with the "other user" precomputed
    qs = (
        Match.objects
        .filter(Q(user1=user) | Q(user2=user), is_active=True)
        .select_related("user1", "user2")
        .annotate(
            other_id=Case(
                When(user1_id=user.id, then=F("user2_id")),
                default=F("user1_id"),
                output_field=IntegerField(),
            ),
            other_username=Case(
                When(user1_id=user.id, then=F("user2__username")),
                default=F("user1__username"),
                output_field=CharField(),
            ),
        )
        .order_by("-created_at")
    )

    # Pagination
    paginator = Paginator(qs, 12)  # 12 cards per page
    page_obj = paginator.get_page(request.GET.get("page"))

    # Counters
    total_matches  = qs.count()
    likes_sent     = Evaluation.objects.filter(evaluator=user, status=Evaluation.LIKE).count()
    likes_received = Evaluation.objects.filter(target=user,    status=Evaluation.LIKE).count()

    # Pending = people who liked me but I haven't evaluated yet
    my_evaluated_ids = Evaluation.objects.filter(evaluator=user).values_list("target_id", flat=True)

    pending_likes_qs = (
        Evaluation.objects
        .filter(target=user, status=Evaluation.LIKE)
        .exclude(evaluator_id__in=my_evaluated_ids)
        .select_related("evaluator")
        .order_by("-updated_at")[:12])

    pending_count = (
        Evaluation.objects
        .filter(target=user, status=Evaluation.LIKE)
        .exclude(evaluator_id__in=my_evaluated_ids)
        .count()
    )

    return render(
    request,
    "matches_list.html",   # << change this line
    {
        "page_obj": page_obj,
        "total_matches": total_matches,
        "likes_sent": likes_sent,
        "likes_received": likes_received,
        "pending_likes": pending_likes_qs,
        "pending_count": pending_count,
    },
)
