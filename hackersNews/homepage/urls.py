from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>', views.index, name='more'),
    path('login/', views.submit),
    path('login/submit/create', views.create),
    path('login/submit/login', views.login),
    path('testProfile',views.testProfile),
    path('testPost',views.testPost)
]