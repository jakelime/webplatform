from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from django.urls import reverse, reverse_lazy
from django_tables2 import SingleTableView


from accounts.models import CustomUser
from accounts.forms import CustomUserChangeForm, CustomUserProfileForm

from .models import Project, Customer, TestParam, TestParamFamily
from .forms import (
    ProjectUpdateForm,
    ProjectCreateForm,
    ProjectApprovalForm,
    TestParamCreateForm,
    TestParamUpdateForm,
)
from .tables import ProjectsListTable

from main.utils import get_time


def maintenance_view(request):
    render("Under maintenance")


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, "Your password was successfully updated!")
            return redirect("change_password")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "accounts/change_password.html", {"form": form})


@login_required()
def infoview_test_family(request):
    context = {"objects": TestParamFamily.objects.all()}
    return render(request, "ptms/info_testfamily.html", context=context)


#################################
## User Profile and Management ##
#################################


class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "ptms/users_list.html"
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
                "is_spock_user": user_obj.has_perm("accounts.is_spock_user"),
                "is_npd": user_obj.has_perm("accounts.is_npd"),
                "is_manager": user_obj.has_perm("accounts.is_manager"),
            }
            objects.append(data)
        context["objects"] = objects
        return context


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "ptms/users_update.html"
    context_object_name = "objects"
    success_url = reverse_lazy("ptms:users_list")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class CustomUserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserProfileForm
    template_name = "ptms/user_profile.html"
    context_object_name = "objects"
    success_url = reverse_lazy("ptms:users_list")


########################
## Project management ##
########################


class ProjectsListView(LoginRequiredMixin, SingleTableView):
    model = Project
    table_class = ProjectsListTable
    template_name = "ptms/projects_list.html"

    def get_queryset(self):
        if not self.request.user.has_perm("accounts.is_spock"):
            queryset = self.model.objects.filter(is_approved=True).exclude(
                customers__name__in=["spock"]
            )
        else:
            queryset = Project.objects.filter(is_approved=True)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class ProjectsStagingListView(PermissionRequiredMixin, SingleTableView):
    permission_required = "accounts.is_npd"
    raise_exception = False
    redirect_field_name = "ptms:home"
    model = Project
    template_name = "ptms/projects_list.html"
    context_object_name = "objects"
    table_class = ProjectsListTable


    def get_queryset(self):
        queryset = Project.objects.filter(is_approved=False).order_by("-date_updated")
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = "ptms/project_create.html"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user_created = self.request.user
        project.log_records = f"{get_time()} - Created by {self.request.user}"
        project.save()
        if self.request.user.username not in project.get_dri():
            project.user_dri.add(self.request.user)
        project.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ptms:project_detail", kwargs={"slug": self.object.slug})


class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = "ptms/project_detail.html"
    context_object_name = "project"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = "ptms/project_update.html"
    context_object_name = "objects"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user_updated = self.request.user
        log_records = self.model.objects.get(pk=project.id).log_records.split("\n")
        if not log_records:
            log_records = []
        log_records.append(f"{get_time()} - Updated by {self.request.user}")
        if len(log_records) < settings.PROJECT_LOG_MAXLENGTH:
            log_records = log_records[: settings.PROJECT_LOG_MAXLENGTH]
        project.log_records = "\n".join(log_records)
        project.save()
        form.clean_user_dri(user=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ptms:project_detail", kwargs={"slug": self.object.slug})


class ProjectApprovalView(PermissionRequiredMixin, UpdateView):
    permission_required = "accounts.is_manager"
    model = Project
    form_class = ProjectApprovalForm
    template_name = "ptms/project_approval.html"
    context_object_name = "object"
    success_url = reverse_lazy("ptms:projects_list")

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["log_records"] = context["object"].log_records.split("/n")
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.user_updated = self.request.user
        log_records = self.model.objects.get(pk=project.id).log_records.split("\n")
        if not log_records:
            log_records = []
        if project.is_approved:
            log_records.append(f"{get_time()} - APPROVED by {self.request.user}")
        else:
            log_records.append(f"{get_time()} - REJECTED by {self.request.user}")
        if len(log_records) < settings.PROJECT_LOG_MAXLENGTH:
            log_records = log_records[: settings.PROJECT_LOG_MAXLENGTH]
        project.log_records = "\n".join(log_records)
        project.save()
        return super().form_valid(form)


################################
## Test Parametric management ##
################################


class TestParamListView(LoginRequiredMixin, SingleTableView):
    model = TestParam
    template_name = "ptms/testparams_list.html"
    table_class = ProjectsListTable
    context_object_name = "objects"

    def get_queryset(self):
        # queryset = Project.objects.filter(is_approved=True).exclude(
        #     customers__name__in=["spock"]
        # )
        queryset = super().get_queryset()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        objects = context["objects"]
        new_objects = []
        for obj in objects:
            data = {}
            data["testparam_obj"] = obj
            test_family_str = "None"
            test_family_list = [tf.name.capitalize() for tf in obj.test_family.all()]
            if len(test_family_list) == 1:
                test_family_str = test_family_list[0]
            elif len(test_family_list) > 1:
                test_family_str = ", ".join(test_family_list)
            data["test_family"] = test_family_str
            new_objects.append(data)
        context["objects"] = new_objects

        return context


class TestParamCreateView(LoginRequiredMixin, CreateView):
    model = TestParam
    form_class = TestParamCreateForm
    template_name = "ptms/testparam_create.html"
    success_url = reverse_lazy("ptms:testparams_list")

    def form_valid(self, form):
        return super().form_valid(form)


class TestParamUpdateView(LoginRequiredMixin, UpdateView):
    model = TestParam
    form_class = TestParamUpdateForm
    template_name = "ptms/testparam_update.html"
    success_url = reverse_lazy("ptms:testparams_list")

    def form_valid(self, form):
        return super().form_valid(form)


class TestParamDetailView(LoginRequiredMixin, DetailView):
    model = TestParam
    template_name = "ptms/testparam_detail.html"
    context_object_name = "object"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        testparam_object = context["object"]
        context["test_families"] = testparam_object.test_family.all()
        return context















