# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Fieldset, Field, Submit, Button
from crispy_forms.bootstrap import (
    AppendedText,
    PrependedText,
    FormActions,
    UneditableField,
)
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.conf import settings

from .models import LabRecord
from accounts.models import CustomUser


class CssMFieldSmall(Div):
    css_class = "col-md-2"


class CssMFieldMedium(Div):
    css_class = "col-md-6"


class LabRecordCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.help_text_inline = True
    helper.layout = Layout(
        Fieldset(
            "Record Information",
            "job_number",
            "record_id",
            "engine_type",
            "engine_make",
        ),
        # Fieldset("engine_type", "engine_make"),
        # Field("engine_type"),
        # Field("engine_make"),
        Fieldset(
            "Microhardness test",
            Div(
                CssMFieldSmall("micro_hardness_meas1"),
                CssMFieldSmall("micro_hardness_meas2"),
                CssMFieldSmall("micro_hardness_meas3"),
                CssMFieldSmall("micro_hardness_meas4"),
                CssMFieldSmall("micro_hardness_meas5"),
                css_class="row gx-5",
            ),
            Div(
                CssMFieldMedium("micro_hardness_meas_avg"),
                CssMFieldMedium("micro_hardness_results"),
                css_class="row gx-5",
            ),
        ),
        # Field("micro_hardness_meas1"),
        # Field("micro_hardness_meas2"),
        # Field("micro_hardness_meas3"),
        # Field("micro_hardness_meas4"),
        # Field("micro_hardness_meas5"),
        # Field("micro_hardness_avg"),
        # Field("micro_hardness_results"),
        FormActions(
            Submit(
                "submit",
                "Register NEW Record",
                css_class="btn btn-primary btn-lg btn-block",
            ),
        ),
    )

    class Meta:
        model = LabRecord
        # fields = "__all__"
        exclude = ("user_created", "user_updated", "log_records", "approval_status")
        # fields = (
        #     "record_id",
        #     "job_number",
        #     "engine_type",
        #     "engine_make",
        # )


class LabRecordUpdateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.help_text_inline = True
    helper.layout = Layout(
        Fieldset(
            "Record Information",
            "job_number",
            "record_id",
            "engine_type",
            "engine_make",
        ),
        Fieldset(
            "Microhardness test",
            Div(
                CssMFieldSmall("micro_hardness_meas1"),
                CssMFieldSmall("micro_hardness_meas2"),
                CssMFieldSmall("micro_hardness_meas3"),
                CssMFieldSmall("micro_hardness_meas4"),
                CssMFieldSmall("micro_hardness_meas5"),
                css_class="row gx-5",
            ),
            Div(
                CssMFieldMedium("micro_hardness_meas_avg"),
                CssMFieldMedium("micro_hardness_results"),
                css_class="row gx-5",
            ),
        ),
        FormActions(
            Submit(
                "submit",
                "Update Record",
                css_class="btn btn-primary btn-lg btn-block",
            ),
        ),
    )

    class Meta:
        model = LabRecord
        exclude = ("user_created", "user_updated", "log_records", "approval_status")


class LabRecordApprovalForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.help_text_inline = True
    helper.layout = Layout(
        Fieldset(
            "Record Information",
            "job_number",
            "record_id",
            "engine_type",
            "engine_make",
        ),
        Fieldset(
            "Microhardness test",
            Div(
                CssMFieldSmall("micro_hardness_meas1"),
                CssMFieldSmall("micro_hardness_meas2"),
                CssMFieldSmall("micro_hardness_meas3"),
                CssMFieldSmall("micro_hardness_meas4"),
                CssMFieldSmall("micro_hardness_meas5"),
                css_class="row gx-5",
            ),
            Div(
                CssMFieldMedium("micro_hardness_meas_avg"),
                CssMFieldMedium("micro_hardness_results"),
                css_class="row gx-5",
            ),
        ),
        Fieldset(
            "READ CAREFULLY!",
            Div(
                CssMFieldMedium("approval_status"),
                css_class="row gx-5",
            ),
        ),
        FormActions(
            Submit(
                "submit",
                "Update APPROVAL",
                css_class="btn btn-primary btn-lg btn-block",
            ),
        ),
    )

    class Meta:
        model = LabRecord
        exclude = ("user_created", "user_updated", "log_records")