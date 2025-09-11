from django.conf import settings
from django.db import models
from django.db.models import Q

# Create your models here.

# matches/models.py
from django.conf import settings
from django.db import models
from django.db.models import Q

class Evaluation(models.Model):
    LIKE = "LIKE"
    UNLIKE = "UNLIKE"   # a.k.a. Pass / Dislike
    STATUS_CHOICES = [(LIKE, "Like"), (UNLIKE, "Unlike")]

    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="evaluations_sent"
    )
    target = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="evaluations_received"
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    decided_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("evaluator", "target")  # one current opinion per pair

    def __str__(self):
        return f"{self.evaluator} → {self.target}: {self.status}"


class Match(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="matches_as_user1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="matches_as_user2")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user1", "user2")

    def __str__(self):
        return f"Match({self.user1} ↔ {self.user2}) active={self.is_active}"

    @staticmethod
    def pair_q(a, b):
        return Q(user1=a, user2=b) | Q(user1=b, user2=a)


