from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# class AccountUser(models.Model):

#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="user_account",
#         null=True,
#     )


# class Profile(models.Model):

#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="profile",
#         null=True,
#     )

#     LANGUAGE_CHOICES = [
#         ("FR", "French"),
#         ("EN", "English"),
#         ("ES", "Spanish"),
#         ("DE", "German"),
#     ]

#     language = models.CharField(
#         max_length=10,
#         choices=LANGUAGE_CHOICES,
#         blank=False,
#         null=False,
#         help_text="Language",
#         default="FR",
#     )

#     phone_number = models.CharField(
#         blank=True, null=True, help_text="Numéro de téléphone"
#     )

#     birth_date = models.DateField(null=True)


class UserAccount(models.Model):
    """
    Informations personnelles liées à l'utilisateur (prénom, nom, email, adresse...)
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_account"
    )

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=False)
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    language = models.CharField(
        max_length=10,
        choices=[
            ("FR", "French"),
            ("EN", "English"),
            ("ES", "Spanish"),
            ("DE", "German"),
        ],
        default="FR",
    )

    def __str__(self):
        return f"Compte de {self.user.username}"
