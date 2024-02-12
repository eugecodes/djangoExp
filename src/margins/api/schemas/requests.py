from ninja import ModelSchema

from margins.models import Margin


class MarginRequest(ModelSchema):
    rate_id: int

    class Config:
        model = Margin
        model_fields = [
            "type",
            "min_consumption",
            "max_consumption",
            "min_margin",
            "max_margin",
        ]
        optional_fields = [
            "min_consumption",
            "max_consumption",
        ]


class MarginUpdateRequest(ModelSchema):
    class Config:
        model = Margin
        model_fields = [
            "type",
            "min_consumption",
            "max_consumption",
            "min_margin",
            "max_margin",
        ]
        optional_fields = [
            "min_consumption",
            "max_consumption",
        ]
