from django.urls import include, path
from . import views

urlpatterns = [
    path('users/', views.users_list),
    path('users/<int:id>/', views.user),
    path('submissions/<int:id>/', views.sub_comment_list),
    path('submissions/<int:id>/', views.get_submission),
    path('users/<int:id>', views.get_user_comments),
    path('users/<int:id>', views.get_user_submissions),
    path('submissions/<int:id>', views.post_comment),
]