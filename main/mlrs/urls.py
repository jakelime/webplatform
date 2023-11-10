from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = "mlrs"

urlpatterns = [
    # path("", views.index, name="index"),
    path(
        "",
        views.LabRecordListView.as_view(template_name="mlrs/records_list.html"),
        name="home",
    ),
    path(
        "records",
        views.LabRecordListView.as_view(template_name="mlrs/records_list.html"),
        name="records_list",
    ),
    path("create_record", views.LabRecordCreate.as_view(), name="create_record"),
    path(
        "record_details/<int:pk>",
        views.LabRecordDetailView.as_view(),
        name="record_details",
    ),
]
