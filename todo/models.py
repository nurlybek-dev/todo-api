from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.IntegerField(blank=True, null=True)
    deadline = models.DateTimeField(blank=True, null=True)
