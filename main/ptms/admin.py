from django.contrib import admin
from .models import Project, ProjectFamily, Customer, BuildPhase
from .models import TestParam,  TestParamFamily


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "date_updated",
    ]
    date_hierarchy = "date_created"
    fieldsets = (
        None,
        {},
    )

    search_fields = ("name", "code", "family", "description", "customers")

    readonly_fields = ("user_created", "user_updated", "log_records")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "is_approved",
                    "name",
                    "code",
                    "family",
                    "customers",
                    "description",
                    "slug",
                ),
            },
        ),
        (
            "Project Build",
            {
                "fields": (
                    "build_phase",
                    "start_date",
                    "poc_date",
                    "p1_date",
                    "evt_date",
                    "dvt_date",
                    "pvt_date",
                    "mp_date",
                ),
            },
        ),
        (
            "Admin",
            {
                "fields": ("user_created", "user_dri", "user_updated", "log_records"),
            },
        ),
    )


class CustomerAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    readonly_fields = ("date_created", "date_updated")


class BuildPhaseAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    readonly_fields = ("date_created", "date_updated")


class ProjectFamilyAdmin(admin.ModelAdmin):
    search_fields = ("name", "description")
    readonly_fields = ("date_created", "date_updated")


admin.site.register(Project, ProjectAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(BuildPhase, BuildPhaseAdmin)
admin.site.register(ProjectFamily, ProjectFamilyAdmin)
admin.site.register(TestParam)
admin.site.register(TestParamFamily)
