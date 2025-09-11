from django.db import models
from django.conf import settings


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

    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(120)],
        help_text="Âge temporaire, à synchroniser avec users plus tard",
    )

    bio = models.TextField(max_length=500, blank=True, help_text="Bio de l'utilisateur")

    photo = models.ImageField(
        upload_to="photos/%Y/%m",
        null=True,
        blank=True,
        help_text="Photo de profil de l'utilisateur",
    )

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

    def interests_list(self):
        if self.interest:
            return [i.strip() for i in self.interest.split(",") if i.strip()]
        return []

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
            return self.photo_url
        return "/media/img/default-profile.png"

    # def photo_url(self):
    #     if self.photo:
    #         return self.photo_url
    #     return "/static/img/default-profile.png"

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_member_profile(sender, instance, created, **kwargs):
        if created:
            MemberProfile.objects.create(user=instance)
