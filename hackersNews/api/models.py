from django.db import models
from rest_framework_api_key.models import AbstractAPIKey

# Create your models here.

class UserAPIKey(AbstractAPIKey):
    user = models.OneToOneField('accounts.HNUser',
                             on_delete=models.CASCADE,
                             related_name="api_keys",
                             )

    def delete(self, *args, **kwargs):
        print("DELETING API KEY")
        if self.user:   # Al eliminar UserAPIKey, borramos el campo key del usuario
            self.user.model.set_api_key("")
        super().delete(*args, **kwargs)
