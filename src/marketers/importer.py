import csv
import io

from common.importer import CsvImporter
from marketers.models import Marketer


class MarketerImporter(CsvImporter):
    @staticmethod
    def run(file):
        messages = {
            "errors": [],
            "updated": 0,
            "created": 0,
        }
        with io.TextIOWrapper(file, encoding="utf-8", newline="\n") as csvfile:
            fieldnames = [
                "",
                "",
                "name",
                "fiscal_name",
                "cif",
                "email",
                "fee",
                "Año del rango consumo",
                "address",
            ]
            reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=",")
            all(next(reader) for i in range(9))

            for el in reader:
                _, created = Marketer.objects.update_or_create(
                    cif=el["cif"],
                    defaults={
                        "name": el["name"],
                        "fiscal_name": el["fiscal_name"],
                        "email": el["email"],
                        "fee": CsvImporter.get_money(el["fee"]),
                    },
                )
                if created:
                    messages["created"] += 1
                else:
                    messages["updated"] += 1

            return messages
