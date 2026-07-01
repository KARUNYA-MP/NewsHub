from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(max_length=100)

    image = models.ImageField(upload_to="category/")

    def __str__(self):
        return self.name


class Article(models.Model):

    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    author = models.ForeignKey(User,on_delete=models.CASCADE)

    title = models.CharField(max_length=300)

    slug = models.SlugField(unique=True)

    summary = models.TextField()

    content = models.TextField()

    image = models.ImageField(upload_to='news/')

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    is_trending = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    image = models.ImageField(
        default="default.png",
        upload_to="profile_pics"
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )

    def __str__(self):
        return self.user.username