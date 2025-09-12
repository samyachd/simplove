from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class ReactivationBackend(ModelBackend):
    """
    Backend qui permet aux utilisateurs désactivés de se connecter
    uniquement pour la réactivation.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            if not user.is_active:
                user.is_active = True
                user.save()
                if request:
                    request.session["welcome_back"] = True
            return user
        return None
