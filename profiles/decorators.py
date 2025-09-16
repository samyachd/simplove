from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from .models import MemberProfile

def profile_required(view_func):

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                profile = MemberProfile.objects.get(user=request.user)
                if not profile.looking_for:
                    return redirect(reverse('profiles:create_profile'))
            except MemberProfile.DoesNotExist:
                return redirect(reverse('profiles:create_profile'))
        return view_func(request, *args, **kwargs)
    return _wrapped_view