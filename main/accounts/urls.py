# accounts/urls.py
from django.urls import path
from django.shortcuts import redirect


from .views import SignUpView
app_name = 'accounts'
urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
]