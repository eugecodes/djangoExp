from decimal import Decimal

from ninja import ModelSchema

from supply_points.models import SupplyPoint


class BasicSupplyPointResponse(ModelSchema):
    counter_price_amount: Decimal = None
    counter_price_currency: str = None

    class Config:
        model = SupplyPoint
        model_fields = [
            "id",
            "energy_type",
            "cups",
            "alias",
            "is_renewable",
            "max_available_power",
            "voltage",
            "counter_type",
            "counter_property",
        ]


class SupplyPointListResponse(ModelSchema):
    class Config:
        model = SupplyPoint
        model_fields = [
            "id",
            "energy_type",
            "cups",
            "alias",
        ]


class SupplyPointDetailResponse(ModelSchema):
    counter_price_amount: Decimal = None
    counter_price_currency: str = None

    class Config:
        model = SupplyPoint
        model_fields = [
            "id",
            "energy_type",
            "cups",
            "alias",
            "is_renewable",
            "max_available_power",
            "voltage",
            "counter_type",
            "counter_property",
        ]
