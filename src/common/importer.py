from decimal import Decimal

from djmoney.money import Money

from config import settings


class CsvImporter:
    @staticmethod
    def get_boolean(value):
        return True if value == "Si" else False

    @staticmethod
    def get_money(value):
        if not value:
            return None
        return Money(
            value.replace(".", "").replace(",", "."), currency=settings.DEFAULT_CURRENCY
        )

    @staticmethod
    def get_decimal(value):
        if not value:
            return None
        return Decimal(value.replace(".", "").replace(",", "."))

    @staticmethod
    def run(file):
        raise NotImplementedError()
