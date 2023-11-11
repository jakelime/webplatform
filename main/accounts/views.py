from django.shortcuts import render

# Create your views here.
# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserProfileForm
from .models import CustomUser


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "accounts/users_list.html"
    context_object_name = "objects"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        user_obj_list = [obj for obj in context["objects"]]
        objects = []
        for user_obj in user_obj_list:
            if user_obj.username == "admin":
                continue
            data = {
                "user_obj": user_obj,
                "is_approver": user_obj.has_perm("accounts.is_approver"),
                "is_manager": user_obj.has_perm("accounts.is_manager"),
            }
            objects.append(data)
        context["objects"] = objects
        return context


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "accounts/update_user.html"
    context_object_name = "objects"
    success_url = reverse_lazy("accounts:users_list")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class CustomUserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserProfileForm
    template_name = "accounts/user_profile.html"
    context_object_name = "objects"
    success_url = reverse_lazy("landing")
