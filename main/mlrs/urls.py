from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = "mlrs"

urlpatterns = [
    # path("", views.index, name="index"),
    path(
        "",
        views.LabRecordHomeView.as_view(template_name="mlrs/records_list.html"),
        name="home",
    ),
    path(
        "records",
        views.LabRecordListView.as_view(template_name="mlrs/records_list.html"),
        name="list_records",
    ),
    path("create_record", views.LabRecordCreate.as_view(), name="create_record"),
    path(
        "record_details/<int:pk>",
        views.LabRecordDetailView.as_view(),
        name="record_details",
    ),
    path(
        "print_record/<int:pk>",
        views.LabRecordPrintView.as_view(),
        name="print_record",
    ),
    path(
        "update_record/<int:pk>",
        views.LabRecordUpdateView.as_view(),
        name="update_record",
    ),
    path(
        "approve_record/<int:pk>",
        views.LabRecordApprovalView.as_view(),
        name="approve_record",
    ),
]
