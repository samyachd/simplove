from django.db import models, connection
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete, post_migrate
import os


class Interest(models.Model):

    DEFAULT_INTERESTS = [
        "Musique",
        "Sport",
        "Cinéma",
        "Voyages",
        "Lecture",
    ]
    name = models.CharField(max_length=255)


class MemberProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="member_profile",
        null=True,
    )

    GENDER_CHOICES = [("H", "Homme"), ("F", "Femme"), ("A", "Autre")]

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default="H",
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
        default="HET",
        blank=False,
        null=False,
        help_text="Orientation sexuelle",
    )

    age = models.PositiveSmallIntegerField(
        null=True,
        blank=False,
        help_text="Âge de l'utilisateur",
        validators=[
            MinValueValidator(18),
            MaxValueValidator(120),
        ],
    )

    bio = models.TextField(max_length=500, blank=True, help_text="Bio de l'utilisateur")

    interests = models.ManyToManyField(Interest, blank=True)

    photo = models.ImageField(
        upload_to="photos/%Y/%m",
        null=True,
        blank=True,
        help_text="Photo de profil de l'utilisateur",
    )

    location = models.CharField(
        max_length=100, blank=True, help_text="Ville de l'utilisateur"
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
        return f"Profil de {self.user.username}" if self.user else "Profil inconnu"

    def full_description(self):
        if self.user:
            desc = f"{self.user.username}<br>{self.get_gender_display()}, {self.age} ans<br>{self.get_orientation_display()}"
            if self.location:
                desc += f", habite à {self.location}"
        else:
            desc = f"Utilisateur inconnu<br>{self.get_gender_display()}, {self.age} ans<br>{self.get_orientation_display()}"
        return desc

    def has_common_interests(self, other_profile):
        return bool(set(self.interests_list()) & set(other_profile.interest_list()))

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return "/media/img/default-profile.png"

    def create_default_interests(sender, **kwargs):
        # Vérifier que la table Interest existe
        if "profiles_interest" in connection.introspection.table_names():
            for name in Interest.DEFAULT_INTERESTS:
                Interest.objects.get_or_create(name=name)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.create(user=instance)


@receiver(post_delete, sender="profiles.MemberProfile")
def delete_profile_photo(sender, instance, **kwargs):
    """Supprimer la photo quand le profil est supprimé"""
    if instance.photo and instance.photo.path and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)


post_migrate.connect(MemberProfile.create_default_interests)
