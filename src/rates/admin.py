from django.contrib import admin

from common.admin.mixins import CsvExportMixin
from rates.importer import RateImporter
from rates.models import Rate


class RateAdmin(admin.ModelAdmin, CsvExportMixin):
    change_list_template = "admin/changelist.html"
    # fieldsets = (
    #     (None, {"fields": ("email", "password")}),
    # )
    list_display = (
        "marketer",
        "name",
        "energy_type",
        "price_type",
        "min_power",
        "max_power",
    )
    list_display_links = ["name"]
    # list_filter = ("", )
    # search_fields = ("",)
    # ordering = ("",)

    service = RateImporter

    def get_urls(self):
        urls = super().get_urls()
        return self.get_csv_urls() + urls


admin.site.register(Rate, RateAdmin)
