from time import time
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.postgres.fields import ArrayField

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

class News(models.Model):
    # id - Implicito 
    title = models.CharField(max_length=255)
    url = models.URLField()
    descendants = ArrayField(ArrayField(models.IntegerField))
    time = models.IntegerField()
    score = models.IntegerField()
    by = models.ForeignKey(User, verbose_name=_("username"), on_delete=models.CASCADE)
    domain = models.URLField()