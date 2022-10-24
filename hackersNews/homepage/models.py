from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.

# Test
class Login(models.Model):
    username = models.CharField(max_length=255)
    username.primary_key=True
    password = models.CharField(max_length=255)

class User(models.Model):
    # id - Implicito
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    karma = models.Field(default=0)

