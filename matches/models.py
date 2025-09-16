from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL


class Evaluation(models.Model):
    LIKE = "LIKE"
    UNLIKE = "UNLIKE"  # pass / dislike
    STATUS_CHOICES = [
        (LIKE, "Like"),
        (UNLIKE, "Unlike"),
    ]

    evaluator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="given_evaluations"
    )
    target = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_evaluations"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    decided_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("evaluator", "target")

    def __str__(self):
        return f"{self.evaluator} → {self.target}: {self.status}"


class Match(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="matches_as_user1"
    )
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="matches_as_user2"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"Match({self.user1} ↔ {self.user2}) active={self.is_active}"

    @staticmethod
    def pair_q(a, b):
        # Helper to query a pair regardless of order
        return Q(user1=a, user2=b) | Q(user1=b, user2=a)
