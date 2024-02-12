import csv
from functools import reduce
from tempfile import NamedTemporaryFile


def recursive_getattr(obj, attr, *args):
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return reduce(_getattr, [obj] + attr.split("."))


def generate_csv_file(filename: str, headers: dict, data: list):
    with NamedTemporaryFile(
        "w", suffix=".csv", prefix=filename, delete=False
    ) as outfile:
        writer = csv.writer(outfile, delimiter=";")
        writer.writerow(headers.values())
        for instance in data:
            row = []
            for attribute in headers.keys():
                try:
                    field = recursive_getattr(instance, attribute)
                except AttributeError:
                    try:
                        related_field, field = attribute.split(":")
                    except ValueError:  # related field None
                        row.append("")
                        continue
                    related_objects = recursive_getattr(instance, related_field)
                    row.append(
                        "|".join(
                            [
                                recursive_getattr(related_obj, field)
                                for related_obj in related_objects
                            ]
                        )
                    )
                    continue
                if type(field) is list:
                    row.append("|".join(field))
                    continue
                row.append(field)
            writer.writerow(row)
        return outfile.name
