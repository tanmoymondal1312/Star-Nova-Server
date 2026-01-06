from django.db import models
from django.contrib.auth.models import User

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

   