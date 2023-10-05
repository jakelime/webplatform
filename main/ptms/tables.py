import django_tables2 as djt
from django_tables2.utils import A
from .models import Project


class ProjectsListTable(djt.Table):

    name = djt.LinkColumn("ptms:project_detail", args=[A("slug")])
    family = djt.Column()
    user_dri = djt.Column()

    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap.html"
        fields = (
            "name",
            "code",
            "family",
            "user_dri",
            "start_date",
            "date_updated",
        )

    def render_name(self, value):
        return f"{value.capitalize()}"

    def render_family(self, value):
        objects = [obj.name.capitalize() for obj in value.all()]
        result = 'none'
        if len(objects) == 1:
            result = objects[0]
        elif len(objects) > 1:
            result = f"{', '.join(objects)}"
        return result

    def render_user_dri(self, value):
        objects_managers = [obj.username for obj in value.all() if obj.has_perm("accounts.is_manager")]
        objects_others = [obj.username for obj in value.all() if not obj.has_perm("accounts.is_manager")]
        objects = sorted(objects_managers) + sorted(objects_others)
        result = 'none'
        if len(objects) == 1:
            result = objects[0]
        elif len(objects) > 1:
            result = f"{', '.join(objects)}"
        return result





class TestParamsListTable(djt.Table):
    class Meta:
        model = Project
        template_name = "django_tables2/bootstrap.html"








