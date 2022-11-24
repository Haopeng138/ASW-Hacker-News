from django.urls import include, path
from . import views

urlpatterns = [
    path('users/', views.users_list),
    path('users/<int:id>/', views.user),
]