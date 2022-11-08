from allauth.account.adapter import DefaultAccountAdapter
from .models import *
import datetime

class HN_AccountAdapter(DefaultAccountAdapter):
    def new_user(self, request):
        user = HNUser()
        user.date_joined = datetime.date.today()
        return user
