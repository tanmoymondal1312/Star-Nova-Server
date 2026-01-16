from django.db import models
from django.contrib.auth.models import User

LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('bn', 'Bangla'),
    ('ta', 'Tamil'),
    ('te', 'Telugu'),
]
EXPERIENCE_LEVEL_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]

class UserData(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
    )

    name = models.CharField(max_length=255, blank=True, null=True)
    experience_level = models.CharField(
        max_length=20,
        choices=EXPERIENCE_LEVEL_CHOICES,
        blank=True,
        null=True
    )

    age = models.PositiveIntegerField(blank=True, null=True)
    classification = models.CharField(max_length=100, blank=True, null=True)


 