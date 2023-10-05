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

from .models import Project, TestParam
from accounts.models import CustomUser

class ProjectCreateForm(forms.ModelForm):
    start_date = forms.DateField(help_text="Format: YYYY-MM-DD")
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.help_text_inline = True
    helper.layout = Layout(
        Field("name"),
        Field("code"),
        Field("family"),
        Field("customers"),
        Field("description"),
        Field("start_date"),
        Field("build_phase"),
        FormActions(
            Submit(
                "submit",
                "Register NEW Project",
                css_class="btn btn-primary btn-lg btn-block",
            ),
        ),
    )

    class Meta:
        model = Project
        fields = (
            "name",
            "code",
            "family",
            "customers",
            "description",
            "start_date",
            "build_phase",
        )


class ProjectUpdateForm(forms.ModelForm):
    start_date = forms.DateField(help_text="Format: YYYY-MM-DD")
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.help_text_inline = True
    helper.layout = Layout(
        Fieldset(
            "",
            "name",
            "code",
            "slug",
            "description",
        ),
        Fieldset(
            "Attributes",
            "family",
            "customers",
        ),
        Fieldset(
            "Project build details",
            "build_phase",
            "start_date",
            "poc_date",
            "p1_date",
            "evt_date",
            "dvt_date",
            "pvt_date",
            "mp_date",
        ),
        Fieldset(
            "Admin",
            "user_created",
            "user_dri",
        ),
        FormActions(Submit("save", "Save changes"), Button("cancel", "Cancel")),
    )

    class Meta:
        model = Project
        exclude = ("is_approved", "user_updated",)

    def clean_user_dri(self, *args, **kwargs):
        if "user" in kwargs:
            qs_user_dri_list = self.cleaned_data['user_dri']
            dri_list_pks = [obj.pk for obj in qs_user_dri_list]
            dri_list_pks.append(kwargs['user'].pk)
            queryset = CustomUser.objects.filter(pk__in=dri_list_pks)
            self.cleaned_data['user_dri'] = queryset
            return queryset

        return self.cleaned_data['user_dri']

class ProjectApprovalForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.help_text_inline = True
    helper.layout = Layout(
        Field("is_approved"),
        FormActions(Submit("save", "Save changes"), Button("cancel", "Cancel")),
    )

    class Meta:
        model = Project
        fields = ("is_approved",)


class TestParamCreateForm(forms.ModelForm):
    # helper = FormHelper()
    # helper.form_class = "form-horizontal"
    # helper.help_text_inline = True
    # helper.layout = Layout(
    #     Field("is_approved"),
    #     FormActions(Submit("save", "Save changes"), Button("cancel", "Cancel")),
    # )

    class Meta:
        model = TestParam
        fields = "__all__"


class TestParamUpdateForm(forms.ModelForm):
    # helper = FormHelper()
    # helper.form_class = "form-horizontal"
    # helper.help_text_inline = True
    # helper.layout = Layout(
    #     Field("is_approved"),
    #     FormActions(Submit("save", "Save changes"), Button("cancel", "Cancel")),
    # )

    class Meta:
        model = TestParam
        fields = "__all__"
