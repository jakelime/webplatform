from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.


class LabRecord(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=False)
    # slug = models.SlugField(null=True, unique=True)
    code = models.CharField(max_length=20, null=True, blank=True)
    job_number = models.TextField(null=True, blank=True, max_length=1000)
    record_id = models.DateField(null=True, blank=True)

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
        if self.code:
            return f"{self.name} ({self.code})"
        return self.name

    def get_absolute_url(self):
        return reverse("labrecords:mlrs_details", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
