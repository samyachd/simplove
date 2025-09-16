from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver


@receiver(user_logged_in)
def reactivate_user(sender, user, request, **kwargs):
    if not user.is_active:
        user.is_active = True
        user.save()
        request.session["reactivated"] = True
