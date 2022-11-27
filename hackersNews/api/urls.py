from django.urls import include, path
from . import views

urlpatterns = [
    path('users/', views.users_list),
    path('users/<int:id>/', views.user),
    path('submissions/<int:id>/', views.sub_comment_list),
    path('submissions/<int:id>/', views.get_submission),
]