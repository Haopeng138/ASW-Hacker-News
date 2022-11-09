from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>', views.index, name='more'),
    path('login/', views.submit,name="login"),
    path('login/submit/create', views.create),
    path('login/submit/login', views.login),
    path('logout',views.logout,name='logout'),
    path('testProfile/',views.testProfile,name='profile'),
    path('testPost/',views.testPost,name='Post'),
    path('testSubmitPost/',views.testSubmitPost,name='testSubmitPost'),
    path('testPostEdit',views.testPostEdit,name='testPostEdit'),
    path('account/', views.account, name='account')
]