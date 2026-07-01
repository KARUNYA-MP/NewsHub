from django.db import models
from django.contrib.auth.models import User
from news.models import Article


class Bookmark(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)

    article = models.ForeignKey(Article,on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user.username