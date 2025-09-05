from django.db import models
from django.conf import settings


# Create your models here.
class MemberProfil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )

    GENDER_CHOICES = [("H", "Homme"), ("F", "Femme"), ("A", "Autre")]

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=False,
        null=False,
        help_text="Genre de l'utilisateur",
    )

    ORIENTATION_CHOICES = [
        ("HET", "Hétéro"),
        ("HOM", "Homosexuel"),
        ("BI", "Bisexuel(le)"),
        ("ATR", "Autre"),
    ]

    orientation = models.CharField(
        max_length=3,
        choices=ORIENTATION_CHOICES,
        blank=False,
        null=False,
        help_text="Orientation sexuelle",
    )

    age = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        help_text="Âge temporaire, à synchroniser avec users plus tard",
    )

    bio = models.TextField(max_length=500, blank=True, help_text="Bio de l'utilisateur")

    # photo = models.ImageField(
    #     upload_to="profiles/photos",
    #     null=True,
    #     blank=True,
    #     help_text="Photo de profil de l'utilisateur",
    # )

    location = models.CharField(
        max_length=100, blank=True, help_text="Ville de l'utilisateur"
    )

    interest = models.TextField(
        blank=True, help_text="Centre d'intérêt séparé par des virgules"
    )

    LOOKING_FOR_CHOICES = [
        ("SERIOUS", "Pour la vie"),
        ("ONE_NIGHT", "Pour une nuit"),
        ("DRINK", "Pour un verre"),
        ("TALK", "Pour discuter"),
    ]

    looking_for = models.CharField(
        max_length=20,
        choices=LOOKING_FOR_CHOICES,
        blank=False,
        help_text="Intention de rencontre",
    )

    def __str__(self):
        return f"Profil de {self.user.username}"
