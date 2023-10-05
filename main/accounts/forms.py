# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_bootstrap5.bootstrap5 import FloatingField

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.layout = Layout(
        FloatingField("email"),
        FloatingField("password1"),
        FloatingField("password2"),
        FormActions(
            Submit("submit", "Register as new user", css_class="btn-primary btn-lg"),
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        email_domain = email.split("@")[-1]
        if email_domain not in settings.ALLOWED_EMAIL_DOMAINS:
            raise ValidationError(
                (f"{email_domain} not allowed. Please use {settings.ALLOWED_EMAIL_DOMAINS}"),
                code="invalid",
            )
        return email


class CustomUserChangeForm(UserChangeForm):
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.layout = Layout(
        Field("email"),
        Field("username"),
        Field(
            "first_name",
        ),
        Field("last_name"),
        Field(
            "preferred_name",
        ),
        Field("groups"),
        Field("is_active"),
        FormActions(
            Submit("submit", "Save", css_class="btn-primary btn-lg"),
        ),
    )

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "last_name",
            "preferred_name",
            "groups",
            "is_active",
        )


class CustomUserProfileForm(UserChangeForm):
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.layout = Layout(
        Field("email"),
        Field("username"),
        Field("preferred_name"),
        Field("first_name"),
        Field("last_name"),
        FormActions(
            Submit("submit", "Save", css_class="btn-primary btn-lg"),
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("email", "username", "preferred_name", "first_name", "last_name")
