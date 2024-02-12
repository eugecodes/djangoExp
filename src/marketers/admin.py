from django.contrib import admin

from common.admin.mixins import CsvExportMixin
from marketers.importer import MarketerImporter
from marketers.models import Marketer


class MarketerAdmin(admin.ModelAdmin, CsvExportMixin):
    change_list_template = "admin/changelist.html"
    list_display = ("id", "name", "cif", "email", "fee")
    # list_filter = ("", )
    # search_fields = ("",)
    # ordering = ("",)

    service = MarketerImporter

    def get_urls(self):
        urls = super().get_urls()
        return self.get_csv_urls() + urls


admin.site.register(Marketer, MarketerAdmin)
