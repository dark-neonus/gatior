from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'blog'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='blog:feed', permanent=False), name='redirect-to-feed'),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('post/<int:pk>/', views.PostDetailsView.as_view(), name='post'),
    path('account/<str:username>/', views.ProfileDetailsView.as_view(), name='account'),
    path('account_settings/', views.AccountSettingsView.as_view(), name='account_settings'),
    path('delete_post/<int:pk>', login_required(views.delete_post), name="delete_post"),
    path('delete_comment/<int:pk>', login_required(views.delete_comment), name="delete_comment"),
    path('like_post_button/<int:pk>', login_required(views.like_post_button), name="like_post_button"),
    path('get_post_liked_status/<int:pk>', login_required(views.get_post_liked_status), name="get_post_liked_status"),
]
