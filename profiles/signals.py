from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.apps import apps
from .models import MemberProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile = apps.get_model("profiles", "MemberProfile")
        MemberProfile.objects.get_or_create(user=instance)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        MemberProfile.objects.create(user=instance)
