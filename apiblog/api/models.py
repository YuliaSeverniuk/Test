from django.db import models
from django.contrib.auth.models import User


class Posts(models.Model):
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Likes(models.Model):
    posts = models.ForeignKey(Posts, related_name='likes', on_delete=models.CASCADE)
    like = models.BooleanField()
    unlike = models.BooleanField()