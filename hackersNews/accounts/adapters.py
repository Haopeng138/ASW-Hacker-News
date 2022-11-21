from allauth.account.adapter import DefaultAccountAdapter
from .models import *
from api.models import UserAPIKey

# NOTE: Seguramente se necessite otro (o el mismio) adaptador para las cuentas/sistema de django-allauth
class HN_AccountAdapter(DefaultAccountAdapter):
    def new_user(self, request):
        print("Account Adapter new_user")
        user = HackerNewsUserManager.create_empty_user()
        return user

    def save_user(self, request, user, form, commit=True):
        print("Account Adapter save_user")
        user = super().save_user(self, request, user, form)
        UserAPIKey.objects.create(user=user)    # TODO: Revisar el punto de creada (quizas social account)
        return user
