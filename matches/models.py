from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.db.models import Q, F
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Like(models.Model):
    """One-direction like: user -> target (unique per pair)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_given",
    )
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_received",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "target"], name="unique_like_user_target"
            ),
        ]

    def __str__(self):
        return f"👍 {self.user} → {self.target}"


class Match(models.Model):
    """
    Mutual like between two users.
    We store (user1, user2) with enforced ordering user1_id < user2_id
    so each pair exists only once. Deactivation keeps history.
    """
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matches_as_user1",
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matches_as_user2",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~Q(user1=F("user2")), name="match_distinct_users"
            ),
            models.UniqueConstraint(
                fields=["user1", "user2"], name="unique_match_pair_ordered"
            ),
        ]

    def save(self, *args, **kwargs):
        # Enforce ordering: store smaller id in user1
        if self.user1_id and self.user2_id and self.user1_id > self.user2_id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"❤️ {self.user1} ↔ {self.user2}"


# -------- Signals: keep Match in sync with Like ----------

@receiver(post_save, sender=Like)
def create_or_reactivate_match(sender, instance: Like, created, **kwargs):
    if not created:
        return
    # If the reciprocal like exists, create/activate the match
    if Like.objects.filter(user=instance.target, target=instance.user).exists():
        u1, u2 = sorted([instance.user_id, instance.target_id])
        match, _ = Match.objects.get_or_create(user1_id=u1, user2_id=u2)
        if not match.is_active:
            match.is_active = True
            match.save(update_fields=["is_active"])


@receiver(post_delete, sender=Like)
def deactivate_match_on_unlike(sender, instance: Like, **kwargs):
    u1, u2 = sorted([instance.user_id, instance.target_id])
    # If the pair is no longer mutual, deactivate the match
    if not (
        Like.objects.filter(user_id=u1, target_id=u2).exists()
        and Like.objects.filter(user_id=u2, target_id=u1).exists()
    ):
        try:
            match = Match.objects.get(user1_id=u1, user2_id=u2)
            if match.is_active:
                match.is_active = False
                match.save(update_fields=["is_active"])
        except Match.DoesNotExist:
            pass


