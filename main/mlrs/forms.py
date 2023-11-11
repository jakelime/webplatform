# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
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


class LabRecordCreateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.help_text_inline = True
    helper.layout = Layout(
        Field("job_number"),
        Field("record_id"),
        Field("engine_type"),
        Field("engine_make"),
        Field("micro_hardness_meas1"),
        Field("micro_hardness_meas2"),
        Field("micro_hardness_meas3"),
        Field("micro_hardness_meas4"),
        Field("micro_hardness_meas5"),
        Field("micro_hardness_avg"),
        Field("micro_hardness_results"),
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
        fields = "__all__"
        # fields = (
        #     "record_id",
        #     "job_number",
        #     "engine_type",
        #     "engine_make",
        # )
