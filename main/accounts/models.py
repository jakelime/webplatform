# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse, reverse_lazy
from .customvalidators import WhitelistEmailValidator
from django.core.validators import EmailValidator
from django.utils.deconstruct import deconstructible
from django.conf import settings


class CustomUser(AbstractUser):
    first_name = models.CharField(blank=True, max_length=20)
    last_name = models.CharField(blank=True, max_length=20)
    preferred_name = models.CharField(blank=True, max_length=20)
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
    )

    class Meta:
        permissions = (
            ("is_approver", "Approves forms"),
            ("is_manager", "Manage users"),
        )

    # add additional fields in here

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.username = self.email.split("@")[0]
        if not self.first_name:
            self.first_name = self.username.split(".")[0]
        if not self.last_name:
            self.last_name = self.username.split(".")[-1]
        if not self.preferred_name:
            self.preferred_name = (
                f"{self.first_name.capitalize()} {self.last_name.capitalize()}"
            )
        return super().save(*args, **kwargs)

    def get_edit_url(self):
        return reverse_lazy("accounts:user_update", kwargs={"pk": self.pk})

    def get_profile_url(self):
        return reverse_lazy("accounts:update_profile", kwargs={"pk": self.pk})
