from email.policy import default
from statistics import mode
from time import time
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

class Noticias(models.Model):
    # id - Implicito 
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    descendants = ArrayField(models.IntegerField(null=True,blank=True),null=True,blank=True)
    time = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    by = models.ForeignKey(User,on_delete=models.CASCADE)
    domain = models.URLField(max_length=255)
    voted = models.BooleanField(default=False)