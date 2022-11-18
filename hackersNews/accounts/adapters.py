from allauth.account.adapter import DefaultAccountAdapter
from .models import *
from api.models import UserAPIKey


class HN_AccountAdapter(DefaultAccountAdapter):
    def new_user(self, request):
        user = HackerNewsUserManager.create_empty_user()
        return user

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(self, request, user, form)
        UserAPIKey.objects.create(user=user)
        return user
