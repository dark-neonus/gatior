from django.urls import path
from django.views.generic import RedirectView
from . import views
from django.contrib.auth import views as auth_views



app_name = 'auth'

urlpatterns = [
    # path('', RedirectView.as_view(pattern_name='blog:feed', permanent=False), name='redirect-to-feed'),
    # path('feed/', views.FeedView.as_view(), name='feed'),
    # path('post/<int:pk>/', views.PostDetailsView.as_view(), name='post'),
    # path('user/<str:username>/', views.ProfileDetailsView.as_view(), name='user'),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path( "register/", views.RegisterView.as_view(), name='register'),
]
