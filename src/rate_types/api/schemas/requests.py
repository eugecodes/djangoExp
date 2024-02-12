from ninja import ModelSchema

from rate_types.models import RateType


class RateTypeRequest(ModelSchema):
    class Config:
        model = RateType
        model_fields = ["name", "energy_type"]
        fields_optional = ["max_power", "min_power"]
