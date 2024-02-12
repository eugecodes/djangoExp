from ninja import ModelSchema

from rate_types.models import RateType


class BasicRateTypeResponse(ModelSchema):
    class Config:
        model = RateType
        model_fields = ["id", "name", "created"]


class RateTypeListResponse(ModelSchema):
    class Config:
        model = RateType
        model_fields = ["id", "name", "created"]


class RateTypeDetailResponse(ModelSchema):
    class Config:
        model = RateType
        model_fields = ["id", "name", "created"]
