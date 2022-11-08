from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.submit),
    path('login/submit/create', views.create),
    path('login/submit/login', views.login),
    path('account/', views.account, name='account')
]