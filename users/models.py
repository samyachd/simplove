from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class AccountUser(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_account",
        null=True,
    )


class Profile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="user_account",
        null=True,
    )

    LANGUAGE_CHOICES = [
        ("FR", "French"),
        ("EN", "English"),
        ("ES", "Spanish"),
        ("DE", "German"),
    ]

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        blank=False,
        null=False,
        help_text="Language",
        default="FR",
    )

    phone_number = models.CharField(
        blank=True, null=True, help_text="Numéro de téléphone"
    )

    birth_date = models.DateField(null=True)
