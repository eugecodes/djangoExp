from ninja import ModelSchema

from costs.models import OtherCost


class OtherCostRequest(ModelSchema):
    class Config:
        model = OtherCost
        model_fields = [
            "name",
            "mandatory",
            "client_types",
            "max_power",
            "min_power",
            "type",
            "quantity",
            "extra_fee",
        ]
        optional_fields = [
            "max_power",
            "min_power",
            "extra_fee",
        ]


class OtherCostUpdateRequest(ModelSchema):
    class Config:
        model = OtherCost
        model_fields = [
            "name",
            "mandatory",
            "client_types",
            "max_power",
            "min_power",
            "type",
            "quantity",
            "extra_fee",
        ]
        optional_fields = [
            "max_power",
            "min_power",
            "extra_fee",
        ]
