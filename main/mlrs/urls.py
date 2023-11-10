from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = "mlrs"

urlpatterns = [
    # path("", views.index, name="index"),
    path("", TemplateView.as_view(template_name="mlrs/home.html"), name="home"),
]