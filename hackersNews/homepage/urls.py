from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # HOMEPAGE
    path('', views.hackernews, name='index'),
    path('<int:page>', views.index, name='more'),
    # SUBMIT
    path('submit/', views.submit,name="submit"),
    # PROFILE
    path('profile/<int:user_id>',views.profile,name='profile'),
    path('profile/<int:user_id>/update', login_required(views.update_profile), name='update_profile'),
    path('profile/<int:user_id>/comments', views.comments, name='comments'),
    path('profile/<int:user_id>/comments/<int:page>', views.comments, name='comments_more'),
    # NEWS
    path('new', views.new, name='new'),
    path('new/<int:page>', views.new, name='new_more'),
    path('hackernews', views.hackernews, name='hackernews'),
    path('hackernews/<int:page>', views.hackernews, name='hackernews_more'),
    path('ask', views.ask, name='ask'),
    path('ask/<int:page>', views.ask, name='ask_more'),
    path('threads', views.threads, name='threads'),
    path('threads/<int:page>', views.threads, name='threads_more'),
    # POST
    path('post/<int:post_id>', views.post, name='post'),
    path('post/<int:post_id>/comment', login_required(views.post_comment), name='post_comment'),
    path('post/<int:post_id>/edit', login_required(views.post_edit), name='post_edit'),
    path('post/<int:post_id>/delete', login_required(views.post_delete), name='post_delete'),
    # COMMENTS
    path('comment/<int:comment_id>', views.comment, name='comment'),
    path('comment/<int:comment_id>/reply', login_required(views.comment_reply), name='comment_reply'),
    path('comment/<int:comment_id>/edit', login_required(views.comment_edit), name='comment_edit'),
    path('comment/<int:comment_id>/delete', login_required(views.comment_delete), name='comment_delete'),
    # UPVOTES
    path('upvote-post', views.upvote_post, name='upvote_post'),
    path('upvote-comment', views.upvote_comment, name='upvote_comment'),
    path('unvote-post', views.unvote_post, name='unvote_post'),
    path('unvote-comment', views.unvote_comment, name='unvote_comment'),
    # USERLIST
    path('user_submissions', views.user_submissions, name='user_submissions'),
    path('user_submissions/<int:page>', views.user_submissions, name='user_submissions_more'),
    path('upvote_post_views',views.upvote_post_views,name='user_post'),
    path('upvote_post_views/<int:page>',views.upvote_post_views,name='user_post_more')
     
]