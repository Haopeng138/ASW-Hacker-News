from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model
from api.models import UserAPIKey

# NOTE: Seguramente se necessite otro (o el mismio) adaptador para las cuentas/sistema de django-allauth
class HN_AccountAdapter(DefaultAccountAdapter):
    def new_user(self, request):
        print("Account Adapter new_user")

        querySet = get_user_model().objects.filter(email__exact="")
        #print("Users without email")
        for user2 in querySet:
            #print(user2.id)
            user2.delete()

        user = get_user_model().objects.create_empty_user()
        #print(user.id)
        return user

    def save_user(self, request, user, form, commit=True):
        print("Account Adapter save_user")
        user = super().save_user(self, request, user, form)
        UserAPIKey.objects.create(user=user)    # TODO: Revisar el punto de creada (quizas social account)
        return user
