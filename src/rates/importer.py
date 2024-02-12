import csv
import io

from clients.choices import ClientTypes
from common.choices import EnergyTypes
from common.importer import CsvImporter
from marketers.models import Marketer
from rate_types.models import RateType
from rates.choices import PriceTypes
from rates.models import Rate


class RateImporter(CsvImporter):
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
                "marketer",
                "name",
                "price_type",
                "energy_type",
                "client_type",
                "rate_type",
                "permanency",
                "length",
                "is_full_renewable",
                "compensation_surplus",
                "compensation_surplus_value",
                "Nombre (r. pot)",
                "min_power",
                "max_power",
                "nombre (r. con)",
                "min_consumption",
                "max_consumption",
                "energy_price_1",
                "energy_price_2",
                "energy_price_3",
                "energy_price_4",
                "energy_price_5",
                "energy_price_6",
                "power_price_1",
                "power_price_2",
                "power_price_3",
                "power_price_4",
                "power_price_5",
                "power_price_6",
                "Nombre - rango pot.",
            ]
            reader = csv.DictReader(csvfile, fieldnames=fieldnames, delimiter=",")
            all(next(reader) for i in range(10))

            for el in reader:
                marketer_name = el["marketer"]
                rate_type_name = el["rate_type"]
                rate_name = el["name"]
                energy_type = RateImporter.get_energy_type(el["energy_type"])
                client_types = RateImporter.get_client_type(el["client_type"])
                try:
                    marketer = Marketer.objects.get(name=marketer_name)
                except Marketer.DoesNotExist:
                    messages["errors"].append(f"Marketer {marketer_name} not found")
                rate_type, created = RateType.objects.get_or_create(
                    name=rate_type_name, energy_type=energy_type
                )

                rate, created = Rate.objects.update_or_create(
                    name=rate_name,
                    marketer=marketer,
                    defaults={
                        "permanency": CsvImporter.get_boolean(el["permanency"]),
                        "length": el["length"],
                        "rate_type": rate_type,
                        "client_types": client_types,
                        "energy_type": energy_type,
                        "price_type": RateImporter.get_price_type(el["price_type"]),
                        "max_power": CsvImporter.get_decimal(el["max_power"]),
                        "min_power": CsvImporter.get_decimal(el["min_power"]),
                        "min_consumption": CsvImporter.get_decimal(
                            el["min_consumption"]
                        ),
                        "max_consumption": CsvImporter.get_decimal(
                            el["max_consumption"]
                        ),
                        "energy_price_1": CsvImporter.get_money(el["energy_price_1"]),
                        "energy_price_2": CsvImporter.get_money(el["energy_price_2"]),
                        "energy_price_3": CsvImporter.get_money(el["energy_price_3"]),
                        "energy_price_4": CsvImporter.get_money(el["energy_price_4"]),
                        "energy_price_5": CsvImporter.get_money(el["energy_price_5"]),
                        "energy_price_6": CsvImporter.get_money(el["energy_price_6"]),
                        "power_price_1": CsvImporter.get_money(el["power_price_1"]),
                        "power_price_2": CsvImporter.get_money(el["power_price_2"]),
                        "power_price_3": CsvImporter.get_money(el["power_price_3"]),
                        "power_price_4": CsvImporter.get_money(el["power_price_4"]),
                        "power_price_5": CsvImporter.get_money(el["power_price_5"]),
                        "power_price_6": CsvImporter.get_money(el["power_price_6"]),
                        "fixed_term_price": None,
                        "is_full_renewable": CsvImporter.get_boolean(
                            el["is_full_renewable"]
                        ),
                        "compensation_surplus": CsvImporter.get_boolean(
                            el["compensation_surplus"]
                        ),
                        "compensation_surplus_value": CsvImporter.get_money(
                            el["compensation_surplus_value"]
                        ),
                    },
                )
                if created:
                    messages["created"] += 1
                else:
                    messages["updated"] += 1
        return messages

    @staticmethod
    def get_client_type(client_type):
        if client_type == "Empresa":
            return [ClientTypes.COMPANY, ClientTypes.SELF_EMPLOYED]
        elif client_type == "Particular":
            return [ClientTypes.PARTICULAR, ClientTypes.SELF_EMPLOYED]
        elif client_type == "Todos":
            return [
                ClientTypes.COMPANY,
                ClientTypes.SELF_EMPLOYED,
                ClientTypes.PARTICULAR,
                ClientTypes.COMMUNITY_OWNERS,
            ]

    @staticmethod
    def get_energy_type(energy_type):
        if energy_type == "Luz":
            return EnergyTypes.ELECTRICITY
        else:
            return EnergyTypes.GAS

    @staticmethod
    def get_price_type(value):
        if value == "Fijo Fijo":
            return PriceTypes.FIXED
        elif value == "Fijo Base":
            return PriceTypes.BASE
        else:
            return PriceTypes.INDEXED
