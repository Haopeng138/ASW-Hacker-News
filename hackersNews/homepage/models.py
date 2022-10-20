from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

class Login(models.Model):
    username = models.CharField(max_length=255)
    username.primary_key=True
    password = models.CharField(max_length=255)