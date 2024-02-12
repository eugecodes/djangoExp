from ninja import ModelSchema

from energy_costs.models import EnergyCost


class BasicEnergyCostResponse(ModelSchema):
    class Config:
        model = EnergyCost
        model_fields = ["id", "created", "code", "concept", "amount"]


class EnergyCostListResponse(ModelSchema):
    class Config:
        model = EnergyCost
        model_fields = ["id", "created", "code", "concept", "amount"]


class EnergyCostDetailResponse(ModelSchema):
    class Config:
        model = EnergyCost
        model_fields = ["id", "created", "code", "concept", "amount"]
