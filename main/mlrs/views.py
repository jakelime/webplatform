import datetime
from django.utils import timezone
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.http import HttpResponse

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

from .models import LabRecord
from .forms import LabRecordCreateForm, LabRecordUpdateForm, LabRecordApprovalForm
from .tables import LabRecordListTable

from main.utils import get_time


# Create your views here.


class LabRecordHomeView(SingleTableView):
    model = LabRecord
    table_class = LabRecordListTable
    template_name = "mlrs/records_list.html"

    def get_queryset(self):
        # today = datetime.date.today()
        today = timezone.now()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)
        queryset = LabRecord.objects.filter(date_updated__gte=last_month)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class LabRecordListView(LoginRequiredMixin, SingleTableView):
    model = LabRecord
    table_class = LabRecordListTable
    template_name = "mlrs/records_list.html"

    def get_queryset(self):
        queryset = LabRecord.objects.all()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class LabRecordCreate(LoginRequiredMixin, CreateView):
    model = LabRecord
    form_class = LabRecordCreateForm
    template_name = "mlrs/create_record.html"

    def form_valid(self, form):
        record = form.save(commit=False)
        record.approval_status = 0
        record.user_created = self.request.user
        record.user_updated = self.request.user
        record.log_records = f"{get_time()} - Created by {self.request.user}"
        record.save()
        return super().form_valid(form)

    # def form_valid(self, form):
    #     project = form.save(commit=False)
    #     project.user_updated = self.request.user
    #     log_records = self.model.objects.get(pk=project.id).log_records.split("\n")
    #     if not log_records:
    #         log_records = []
    #     if project.is_approved:
    #         log_records.append(f"{get_time()} - APPROVED by {self.request.user}")
    #     else:
    #         log_records.append(f"{get_time()} - REJECTED by {self.request.user}")
    #     if len(log_records) < settings.PROJECT_LOG_MAXLENGTH:
    #         log_records = log_records[: settings.PROJECT_LOG_MAXLENGTH]
    #     project.log_records = "\n".join(log_records)
    #     project.save()
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mlrs:record_details", kwargs={"pk": self.object.pk})


class LabRecordUpdateView(LoginRequiredMixin, UpdateView):
    model = LabRecord
    form_class = LabRecordUpdateForm
    template_name = "mlrs/update_record.html"

    def form_valid(self, form):
        record = form.save(commit=False)
        record.user_updated = self.request.user
        record.log_records = f"{get_time()} - Updated by {self.request.user}"
        record.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mlrs:record_details", kwargs={"pk": self.object.pk})


class LabRecordApprovalView(LoginRequiredMixin, UpdateView):
    model = LabRecord
    form_class = LabRecordApprovalForm
    template_name = "mlrs/update_record.html"

    def form_valid(self, form):
        record = form.save(commit=False)
        record.user_updated = self.request.user
        log_records = self.model.objects.get(pk=record.id).log_records.split("\n")
        if not log_records:
            log_records = []
        log_records.append(
            f"{get_time()} - APPROVAL CHANGE to {record.approval_status} by {self.request.user}"
        )
        if len(log_records) < settings.RECORD_LOG_MAXLENGTH:
            log_records = log_records[: settings.RECORD_LOG_MAXLENGTH]
        record.log_records = "\n".join(log_records)
        record.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mlrs:record_details", kwargs={"pk": self.object.pk})


class LabRecordDetailView(LoginRequiredMixin, DetailView):
    model = LabRecord
    template_name = "mlrs/record_details.html"
    context_object_name = "record"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class LabRecordPrintView(LoginRequiredMixin, DetailView):
    model = LabRecord
    template_name = "mlrs/print_record.html"
    context_object_name = "record"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
