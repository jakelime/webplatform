from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
# import .views

from django.views.generic.base import TemplateView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="landing"),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("ptms/", include("ptms.urls"), name="ptms"),

]

if settings.MAINTENANCE_MODE:
    urlpatterns.insert(0, re_path(r'^', TemplateView.as_view(template_name="maintenance.html"), name="maintenance"))