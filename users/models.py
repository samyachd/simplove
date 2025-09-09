from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    
    username = models.OneToOneField(User, on_delete=models.CASCADE)

    LANGUAGE_CHOICES = [("FR", "French"), ("EN", "English"), ("ES", "Spanish"), ("DE", "German")]

    language = models.CharField(
        max_length=10, 
        choices=LANGUAGE_CHOICES, 
        blank=False, 
        null=False, 
        help_text="Language", 
        default="FR")
    
    phone_number = models.CharField(blank=True, 
                                    null=True, 
                                    help_text="Numéro de téléphone")

    birth_date = models.DateField()