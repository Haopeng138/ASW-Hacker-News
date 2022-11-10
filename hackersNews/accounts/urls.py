from django.urls import path
from . import views

urlpatterns = [
    path('', views.account , name="login"),        # Log in / Sign up
    path('logout/', views.logout , name="logout"),   # Log out
    path('reset_password/', views.account , name="reset_password"),  # Reset password
    path('modify_password/', views.account , name="modify_password"), # Reset password
]