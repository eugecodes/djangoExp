from ninja import ModelSchema

from margins.models import Margin


class BasicMarginResponse(ModelSchema):
    class Config:
        model = Margin
        model_fields = [
            "id",
            "type",
            "min_consumption",
            "max_consumption",
            "min_margin",
            "max_margin",
        ]


class MarginListResponse(ModelSchema):
    class Config:
        model = Margin
        model_fields = [
            "id",
            "type",
        ]


class MarginDetailResponse(ModelSchema):
    class Config:
        model = Margin
        model_fields = [
            "id",
            "type",
            "min_consumption",
            "max_consumption",
            "min_margin",
            "max_margin",
        ]
