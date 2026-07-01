from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    profile_image = models.ImageField(
        upload_to='profile/',
        default='default.png'
    )

    phone = models.CharField(max_length=15)

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username