from django.urls import include, path
from . import views

urlpatterns = [
    # USERS
    path('users/', views.user_list.as_view()),
    path('users/<int:id>/', views.user_detail.as_view()),
    path('users/<int:id>/comments', views.user_comments.as_view()),
    path('users/<int:id>/submission', views.user_submissions.as_view()),
    # SUBMISSIONS
    path('submissions/', views.submission_list.as_view()),
    path('submissions/<int:id>/', views.get_submission),
    path('submissions/<int:id>/comments', views.sub_comment_list),

    # UPVOTE
    path('upvote-post/<int:id>/', views.upvote_post, name='upvote_post'),
    path('upvote-comment/<int:id>/', views.upvote_comment, name='upvote_comment'),
    path('unvote-post/<int:id>/', views.unvote_post, name='unvote_post'),
    path('unvote-comment/<int:id>/', views.unvote_comment, name='unvote_comment'),
]