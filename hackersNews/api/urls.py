from django.urls import include, path
from . import views

urlpatterns = [
    # USERS
    path('users/', views.users_list),
    path('users/<int:id>/', views.user),
    # SUBMISSIONS
    path('submissions/<int:id>/', views.sub_comment_list),
    path('submissions/<int:id>/', views.get_submission),
    # UPVOTE
    path('upvote-post/<int:id>/', views.upvote_post, name='upvote_post'),
    path('upvote-comment/<int:id>/', views.upvote_comment, name='upvote_comment'),
    path('unvote-post/<int:id>/', views.unvote_post, name='unvote_post'),
    path('unvote-comment/<int:id>/', views.unvote_comment, name='unvote_comment'),
]