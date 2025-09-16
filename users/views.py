from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.models import User
from .forms import RegisterForm, AccountForm
from profiles.decorators import profile_required
from .models import UserAccount


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                # Création manuelle pour ignorer l'ancien compte supprimé
                user = User.objects.create_user(
                    username=form.cleaned_data["username"],
                    email=form.cleaned_data["email"],
                    password=form.cleaned_data["password"],
                )
                # Nécessaire pour login() avec plusieurs backends
                user.backend = "django.contrib.auth.backends.ModelBackend"
                login(request, user)
                return redirect("users:create_account")

            except IntegrityError:
                messages.error(
                    request, "Ce nom d’utilisateur ou email est déjà utilisé."
                )
        else:
            messages.error(
                request,
                "Une erreur est survenue dans le formulaire. Merci de vérifier les champs.",
            )
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def create_account(request):
    """
    Compléter les informations du compte (interne) après l'inscription.
    Puis rediriger vers create_profile pour compléter le profil public.
    """
    account, created = UserAccount.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été créé avec succès !")
            # Redirection vers la page pour compléter le profil public
            return redirect("profiles:create_profile")
    else:
        form = AccountForm(instance=account)

    context = {"form": form} | {"hide_navbar": True}
    return render(request, "registration/create_account.html", context)


@login_required
@profile_required
def account_view(request):
    """Afficher les infos du compte personnel"""
    account, created = UserAccount.objects.get_or_create(user=request.user)
    return render(request, "registration/account.html", {"account": account})


@login_required
@profile_required

def account_edit(request):
    """Modifier les infos du compte personnel"""
    account, created = UserAccount.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre compte a été mis à jour.")
            return redirect("users:account")
    else:
        form = AccountForm(instance=account)

    return render(request, "registration/account_edit.html", {"form": form})

@login_required
@profile_required
def manage_account(request):
    """
    Gestion du compte : suppression ou désactivation.
    """
    if request.method == "POST":
        action = request.POST.get("action")
        user = request.user

        if action == "delete":
            logout(request)
            user.delete()  # Supprime User + MemberProfile + Matches + Evaluations (CASCADE)
            messages.success(request, "Votre compte a été supprimé définitivement.")
            return redirect("core:core")

        elif action == "deactivate":
            user.is_active = False
            user.save()
            logout(request)
            messages.info(
                request,
                "Votre compte a été désactivé. Vous pourrez le réactiver en vous reconnectant.",
            )
            return redirect("core:core")

    return render(request, "registration/manage_account.html")


@receiver(user_logged_in)
def reactivate_user(sender, user, request, **kwargs):
    """
    Si un utilisateur désactivé se reconnecte :
    - réactive son compte
    - redirige vers une page de bienvenue
    """
    if not user.is_active:
        user.is_active = True
        user.save()
        request.session["welcome_back"] = True


@login_required
@profile_required
def welcome_back(request):
    """
    Page intermédiaire affichée seulement si l'utilisateur vient d'être réactivé.
    """
    if request.session.pop("welcome_back", False):
        return render(request, "registration/welcome_back.html", {"user": request.user})
    return redirect("core:core")
