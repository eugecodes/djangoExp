from ninja import ModelSchema
from contracts.models import Contract


class BasicContractResponse(ModelSchema):
    class Config:
        model = Contract
        model_fields = ["id", "created"]


class ContractListResponse(ModelSchema):
    class Config:
        model = Contract
        model_fields = ["id", "created"]


class ContractDetailResponse(ModelSchema):
    class Config:
        model = Contract
        model_fields = ["id", "created"]

