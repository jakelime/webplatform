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
from .forms import LabRecordCreateForm
from .tables import LabRecordListTable

from main.utils import get_time


# Create your views here.


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
        record.user_created = self.request.user
        record.log_records = f"{get_time()} - Created by {self.request.user}"
        record.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("mlrs:record_details", kwargs={"pk": self.pk})


class LabRecordDetailView(LoginRequiredMixin, DetailView):
    model = LabRecord
    template_name = "mlrs/record_details.html"
    context_object_name = "record"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context
