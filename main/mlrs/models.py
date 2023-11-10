from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.


class LabRecord(models.Model):
    record_id = models.CharField(null=True, blank=True, max_length=50)
    job_number = models.CharField(null=True, blank=True, max_length=50)
    engine_type = models.CharField(
        max_length=100, null=False, blank=False, unique=False
    )
    engine_make = models.CharField(
        max_length=100, null=False, blank=False, unique=False
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user_created = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_user_created",
    )
    user_updated = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_user_updated",
    )

    log_records = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        return f"{self.pk:05d}-{self.engine_make}"

    def get_absolute_url(self):
        return reverse("mlrs:record_details", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
