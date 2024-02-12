from ninja import ModelSchema

from energy_costs.models import EnergyCost


class EnergyCostRequest(ModelSchema):
    class Config:
        model = EnergyCost
        model_fields = [
            "code",
            "concept",
            "amount",
        ]
        optional_fields = []


class EnergyCostUpdateRequest(ModelSchema):
    class Config:
        model = EnergyCost
        model_fields = [
            "code",
            "concept",
            "amount",
        ]
        optional_fields = []
