from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:page>', views.index, name='more'),
    path('login/', views.submit,name="login"),
    path('login/submit/create', views.create),
    path('login/submit/login', views.login),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    #path('logout',views.logout,name='logout'),
    path('testProfile/',views.testProfile,name='profile'),
    path('testPost/',views.testPost,name='Post'),
    path('testSubmitPost/',views.testSubmitPost,name='testSubmitPost'),
    path('testPostEdit',views.testPostEdit,name='testPostEdit'),
    path('account/', views.account, name='account')
]