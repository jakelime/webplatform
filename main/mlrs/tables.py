import django_tables2 as djt
from django_tables2.utils import A
from .models import LabRecord


class LabRecordListTable(djt.Table):
    record_id = djt.LinkColumn("mlrs:record_details", args=[A("pk")])

    class Meta:
        model = LabRecord
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "record_id",
            "engine_type",
            "engine_make",
            "date_updated",
            "user_created",
            "approval_status"
        )

    def render_engine_type(self, value):
        return f"{value.capitalize()}"


class RecordListTable2(djt.Table):
    class Meta:
        model = LabRecord
        template_name = "django_tables2/bootstrap.html"
