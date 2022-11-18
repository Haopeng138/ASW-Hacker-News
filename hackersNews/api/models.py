from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

# Create your models here.

class UserAPIKey(AbstractAPIKey):
    user = models.ForeignKey('accounts.HNUser',
                             on_delete=models.CASCADE,
                             related_name="api_keys",
                             #unique=True,
                             )
