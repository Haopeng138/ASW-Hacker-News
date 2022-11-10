from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # HOMEPAGE
    path('', views.hackernews, name='index'),
    path('<int:page>', views.index, name='more'),
    path('submit/', views.submit,name="submit"),
    # path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # path('logout',views.logout,name='logout'),
    # path('testProfile/',views.testProfile,name='profile'),
    # PROFILE
    path('profile/<int:user_id>',views.profile,name='profile'),
    path('profile/<int:user_id>/update', login_required(views.update_profile), name='update_profile'),
    # path('testPost/',views.testPost,name='Post'),
    # path('testSubmitPost/',views.testSubmitPost,name='testSubmitPost'),
    # path('testPostEdit',views.testPostEdit,name='testPostEdit'),
    # path('account/', views.account, name='account'),
    path('new', views.new, name='new'),
    path('new/<int:page>', views.new, name='new_more'),
    path('hackernews', views.hackernews, name='hackernews'),
    path('hackernews/<int:page>', views.hackernews, name='hackernews_more'),
    path('ask', views.ask, name='ask'),
    path('ask/<int:page>', views.ask, name='ask_more'),
    path('threads', views.threads, name='threads'),
    path('threads/<int:page>', views.threads, name='threads_more'),
    path('post/<int:post_id>', views.post, name='post'),
    path('post/<int:post_id>/comment', login_required(views.post_comment), name='post_comment'),
    path('post/<int:post_id>/edit', login_required(views.post_edit), name='post_edit'),
    path('post/<int:post_id>/delete', login_required(views.post_delete), name='post_delete'),
    path('upvote-post', views.upvote_post, name='upvote_post'),
    path('upvote-comment', views.upvote_comment, name='upvote_comment'),
    path('comment/<int:comment_id>', views.comment, name='comment'),
    path('comment/<int:comment_id>/reply', login_required(views.comment_reply), name='comment_reply'),
    path('comment/<int:comment_id>/edit', login_required(views.comment_edit), name='comment_edit'),
    path('comment/<int:comment_id>/delete', login_required(views.comment_delete), name='comment_delete'),
]