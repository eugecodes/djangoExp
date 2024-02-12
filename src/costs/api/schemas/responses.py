from ninja import ModelSchema

from costs.models import OtherCost


class BasicOtherCostResponse(ModelSchema):
    class Config:
        model = OtherCost
        model_fields = [
            "id",
            "created",
            "name",
            "mandatory",
            "client_types",
            "max_power",
            "min_power",
            "type",
            "quantity",
            "extra_fee",
        ]


class OtherCostListResponse(ModelSchema):
    class Config:
        model = OtherCost
        model_fields = [
            "id",
            "name",
        ]


class OtherCostDetailResponse(ModelSchema):
    class Config:
        model = OtherCost
        model_fields = [
            "id",
            "created",
            "name",
            "mandatory",
            "client_types",
            "max_power",
            "min_power",
            "type",
            "quantity",
            "extra_fee",
        ]
