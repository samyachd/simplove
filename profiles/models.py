from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, post_migrate
from utils.supabase_client import get_supabase
from .storage_backends import SupabaseMediaStorage


class Interest(models.Model):
    DEFAULT_INTERESTS = ["Musique", "Sport", "Cinéma", "Voyages", "Lecture"]
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class MemberProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="member_profile",
    )

    GENDER_CHOICES = [("H", "Homme"), ("F", "Femme"), ("A", "Autre")]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="H")

    ORIENTATION_CHOICES = [
        ("HET", "Hétéro"),
        ("HOM", "Homosexuel"),
        ("BI", "Bisexuel(le)"),
        ("ATR", "Autre"),
    ]
    orientation = models.CharField(
        max_length=3, choices=ORIENTATION_CHOICES, default="HET"
    )

    age = models.PositiveSmallIntegerField(
        null=True, validators=[MinValueValidator(18), MaxValueValidator(120)]
    )

    bio = models.TextField(max_length=500, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)

    photo = models.ImageField(
        upload_to="photos",
        null=True,
        blank=True,
        storage=SupabaseMediaStorage(),
    )
    location = models.CharField(max_length=100, blank=True)

    LOOKING_FOR_CHOICES = [
        ("SERIOUS", "Pour la vie"),
        ("ONE_NIGHT", "Pour une nuit"),
        ("DRINK", "Pour un verre"),
        ("TALK", "Pour discuter"),
    ]
    looking_for = models.CharField(
        max_length=20, choices=LOOKING_FOR_CHOICES, blank=False
    )

    def __str__(self):
        return f"Profil de {self.user.username}"

    def photo_url(self):
        """
        Renvoie l'URL publique du fichier stocké dans Supabase.
        Si pas de photo, renvoie l'image par défaut.
        """
        if self.photo:
            try:
                return self.photo.url  # Utilise la méthode url du storage backend
            except Exception as e:
                print(f"[MemberProfile] Erreur récupération URL photo: {e}")
        return f"{settings.SUPABASE_PUBLIC_URL}/img/default-profile.png"

    @staticmethod
    def create_default_interests(sender, **kwargs):
        from django.db import connection

        if "profiles_interest" in connection.introspection.table_names():
            for name in Interest.DEFAULT_INTERESTS:
                Interest.objects.get_or_create(name=name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.create(user=instance)
