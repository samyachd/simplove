from django.shortcuts import render
from django.http import HttpResponse.
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from .models import Like, Match

User = get_user_model()

@login_required
def like_user(request, user_id):
    if request.user.id == user_id:
        return HttpResponseBadRequest("Cannot like yourself.")
    target = User.objects.get(pk=user_id)
    Like.objects.get_or_create(user=request.user, target=target)
    return redirect("my_matches")

@login_required
def unlike_user(request, user_id):
    Like.objects.filter(user=request.user, target_id=user_id).delete()
    return redirect("my_matches")

@login_required
def my_matches(request):
    me = request.user.id
    matches = (
        Match.objects
        .filter(Q(user1_id=me) | Q(user2_id=me), is_active=True)
        .select_related("user1", "user2")
    )
    return render(request, "matches/matches_list.html", {"matches": matches})
