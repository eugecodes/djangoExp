from django.contrib.messages import SUCCESS, ERROR
from django.shortcuts import render, redirect
from django.urls import path

from common.admin.forms import CsvImportForm
from common.importer import CsvImporter


class CsvExportMixin:
    change_list_template = "admin/changelist.html"

    service: CsvImporter() = None

    def get_csv_urls(self):
        my_urls = [
            path("import-csv/", self.import_csv),
        ]
        return my_urls

    def import_csv(self, request):
        if request.method == "POST":
            messages = self.service.run(request.FILES["csv_file"])
            for error in messages["errors"]:
                self.message_user(request, error, ERROR)
            self.message_user(
                request, f"{messages['created']} rows successfully created", SUCCESS
            )
            self.message_user(
                request, f"{messages['updated']} rows successfully updated", SUCCESS
            )
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "admin/csv_form.html", payload)
