from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class created_forms(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)

class complited_forms(models.Model):
    respondent = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField(blank=True, null=True)
