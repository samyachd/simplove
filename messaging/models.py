from django.db import models
<<<<<<< HEAD

# Create your models here.
=======
from django.contrib.auth.models import User

class Thread(models.Model):
    participants = models.ManyToManyField(User, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return " - ".join([u.username for u in self.participants.all()])

class Message(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.content[:20]}"
>>>>>>> origin/messaging
