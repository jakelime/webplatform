from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy

# Create your models here.


class LabRecord(models.Model):
    class ApprovalStatus(models.TextChoices):
        PENDING = 0, gettext_lazy("Pending")
        APPROVED = 1, gettext_lazy("Approved")
        REJECTED = 2, gettext_lazy("Rejected")
        C_APPROVED = 3, gettext_lazy("ConditionalApproval")

    class TestResult(models.TextChoices):
        NIL = 0, gettext_lazy("NIL")
        PASS = 1, gettext_lazy("PASS")
        FAIL = 2, gettext_lazy("FAIL")

    approval_status = models.CharField(
        max_length=20, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING
    )
    record_id = models.CharField(null=True, blank=True, max_length=50)
    job_number = models.CharField(null=True, blank=True, max_length=50)
    engine_type = models.CharField(
        max_length=100, null=False, blank=False, unique=False
    )
    engine_make = models.CharField(
        max_length=100, null=False, blank=False, unique=False
    )

    micro_hardness_descr = models.TextField(null=True, blank=True, max_length=1000)
    micro_hardness_meas1 = models.FloatField(null=True, blank=True)
    micro_hardness_meas2 = models.FloatField(null=True, blank=True)
    micro_hardness_meas3 = models.FloatField(null=True, blank=True)
    micro_hardness_meas4 = models.FloatField(null=True, blank=True)
    micro_hardness_meas5 = models.FloatField(null=True, blank=True)
    micro_hardness_meas_avg = models.FloatField(null=True, blank=True)
    micro_hardness_results = models.CharField(
        max_length=5, choices=TestResult.choices, default=TestResult.NIL
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

    def get_edit_url(self):
        return reverse("mlrs:update_record", kwargs={"pk": self.pk})

    def get_approve_url(self):
        return reverse("mlrs:approve_record", kwargs={"pk": self.pk})

    def get_print_url(self):
        return reverse("mlrs:print_record", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_log_records_list(self):
        if isinstance(self.log_records, str):
            return self.log_records.split("/n")
        else:
            return ["error"]
