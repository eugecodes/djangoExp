from decimal import Decimal

from djmoney.money import Money
from ninja import ModelSchema

from supply_points.models import SupplyPoint


class SupplyPointRequest(ModelSchema):
    channel_id: int = None
    client_id: int
    address_id: int
    counter_price_amount: Decimal = None
    counter_price_currency: str = None
    counter_price: Money = None

    class Config:
        model = SupplyPoint
        model_fields = [
            "energy_type",
            "cups",
            "alias",
            "is_renewable",
            "max_available_power",
            "voltage",
            "counter_type",
            "counter_property",
        ]
        optional_fields = [
            "energy_type",
            "cups",
            "alias",
            "is_renewable",
            "max_available_power",
            "voltage",
            "counter_type",
            "counter_property",
        ]
        arbitrary_types_allowed = True


class SupplyPointUpdateRequest(ModelSchema):
    address_id: int
    counter_price_amount: Decimal = None
    counter_price_currency: str = None
    counter_price: Money = None

    class Config:
        model = SupplyPoint
        model_fields = [
            "energy_type",
            "cups",
            "alias",
            "is_renewable",
            "max_available_power",
            "voltage",
            "counter_type",
            "counter_property",
        ]
        optional_fields = [
            "energy_type",
            "cups",
            "alias",
            "is_renewable",
            "max_available_power",
            "voltage",
            "counter_type",
            "counter_property",
        ]
        arbitrary_types_allowed = True
