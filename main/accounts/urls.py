# accounts/urls.py
from django.urls import path
from django.shortcuts import redirect

from django.views.generic.base import TemplateView
from . import views


app_name = "accounts"
urlpatterns = [
    path("", views.CustomUserListView.as_view(), name="user_list"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path(
        "create_user",
        TemplateView.as_view(template_name="accounts/users_create.html"),
        name="users_create",
    ),
    path("users/<int:pk>", views.CustomUserUpdateView.as_view(), name="user_update"),
    path(
        "update_profile/<int:pk>",
        views.CustomUserProfileUpdateView.as_view(),
        name="update_profile",
    ),
]
