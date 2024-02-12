from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from saving_studies.models import SavingStudy


class SavingStudyAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    # )
    list_display = ("id", "created")
    # list_filter = ("", )
    # search_fields = ("",)
    # ordering = ("",)


admin.site.register(SavingStudy, SavingStudyAdmin)
