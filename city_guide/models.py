from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Place(models.Model):
    image_url = models.URLField()
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.ForeignKey("Place", on_delete=models.CASCADE, related_name="comments")
    question = models.ForeignKey("Question", on_delete=models.CASCADE, null=True, blank=True, related_name="comments")
    text = models.TextField()
    media_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.created_at} {self.user.username} {self.place.name}"


class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    place = models.ForeignKey("Place", on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return f"{self.created_at} {self.user.username} {self.place.name}"


class User(AbstractUser):
    pass
