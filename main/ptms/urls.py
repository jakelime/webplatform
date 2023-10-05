from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.shortcuts import redirect


from . import models, views

app_name = 'ptms'

urlpatterns = [
    path("", TemplateView.as_view(template_name="ptms/home.html"), name="home"),

    path("users", views.CustomUserListView.as_view(), name="users_list"),
    path("user_profile/<int:pk>", views.CustomUserProfileUpdateView.as_view(), name="user_profile"),
    path("users/create_user", TemplateView.as_view(template_name="ptms/users_create.html"), name="users_create"),
    path("users/<int:pk>", views.CustomUserUpdateView.as_view(), name="users_update"),

    path("projects", views.ProjectsListView.as_view(), name="projects_list"),
    path("projects/create", views.ProjectCreateView.as_view(), name="project_create"),
    path("projects/staging", views.ProjectsStagingListView.as_view(), name="projects_list_staging"),
    path("projects/approval/<slug:slug>", views.ProjectApprovalView.as_view(), name="project_approval"),
    path("projects/update/<slug:slug>", views.ProjectUpdateView.as_view(), name="project_update"),
    path("projects/<slug:slug>", views.ProjectDetailView.as_view(), name="project_detail"),

    path("testparams", views.TestParamListView.as_view(), name="testparams_list"),
    path("testparams/info", views.infoview_test_family, name="testparams_info"),
    path("testparams/create", views.TestParamCreateView.as_view(), name="testparam_create"),
    path("testparams/update/<slug:slug>", views.TestParamUpdateView.as_view(), name="testparam_update"),
    path("testparams/<slug:slug>", views.TestParamDetailView.as_view(), name="testparam_detail"),


]
