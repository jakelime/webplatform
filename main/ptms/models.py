from django.db import models
from django.template.defaultfilters import slugify  # new
from django.urls import reverse
from django.conf import settings


class Project(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=False)
    slug = models.SlugField(null=True, unique=True)
    code = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True, max_length=1000)
    start_date = models.DateField(null=True, blank=True)
    poc_date = models.DateField(null=True, blank=True)
    p1_date = models.DateField(null=True, blank=True)
    evt_date = models.DateField(null=True, blank=True)
    dvt_date = models.DateField(null=True, blank=True)
    pvt_date = models.DateField(null=True, blank=True)
    mp_date = models.DateField(null=True, blank=True)
    # family = models.CharField(max_length=20, null=True, blank=True, default="others")
    family = models.ManyToManyField("ProjectFamily", blank=True)
    customers = models.ManyToManyField("Customer", blank=True)
    build_phase = models.ForeignKey(
        "BuildPhase", blank=True, null=True, on_delete=models.SET_NULL
    )
    is_approved = models.BooleanField(default=False)
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
    user_dri = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_user_dri",
        blank=False,
    )
    log_records = models.TextField(null=True, blank=True, default="")

    def __str__(self):
        if self.code:
            return f"{self.name} ({self.code})"
        return self.name

    def get_absolute_url(self):
        return reverse("ptms:project_detail", kwargs={"slug": self.slug})  # new

    def get_edit_url(self):
        return reverse("ptms:project_update", kwargs={"slug": self.slug})  # new

    def get_approval_url(self):
        return reverse("ptms:project_approval", kwargs={"slug": self.slug})  # new

    def get_dri(self):
        dri_list = [user.username for user in self.user_dri.all()]
        if len(dri_list) == 1:
            return dri_list[0]
        elif len(dri_list) > 1:
            return ", ".join(dri_list)
        else:
            return "none"

    def get_dri_objects(self):
        return [obj for obj in self.user_dri.all()]

    def get_project_families(self):
        xlist = [x.name.capitalize() for x in self.family.all()]
        if len(xlist) == 1:
            return xlist[0]
        elif len(xlist) > 1:
            return ", ".join(xlist)
        else:
            return "none"

    def get_customers(self):
        customers = [x.name.capitalize() for x in self.customers.all()]
        if len(customers) == 1:
            return customers[0]
        elif len(customers) > 1:
            return ", ".join(customers)
        else:
            return "none"

    def get_log_records_list(self):
        return self.log_records.split("/n")

    def save(self, *args, **kwargs):
        if self.code:
            self.code = self.code.upper()
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TestParam(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    slug = models.SlugField(null=True, unique=True, blank=True)
    test_family = models.ManyToManyField("TestParamFamily", blank=True)
    test_attr1 = models.CharField(
        max_length=50, null=False, blank=False, default="others"
    )
    test_attr2 = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True, max_length=1000)
    driving_condition = models.TextField(null=True, blank=True, max_length=1000)
    expected_value = models.FloatField(null=True, blank=True)
    usl = models.FloatField(null=True, blank=True)
    lsl = models.FloatField(null=True, blank=True)
    units = models.CharField(null=True, blank=True, max_length=10)
    project = models.ForeignKey(
        "Project", blank=True, null=True, on_delete=models.SET_NULL
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.project}-{self.name}")
        super().save(*args, **kwargs)


class Customer(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class BuildPhase(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True, max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectFamily(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True, max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TestParamFamily(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True, max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
