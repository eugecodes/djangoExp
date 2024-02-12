from ninja import ModelSchema

from clients.models import Client


class BasicClientResponse(ModelSchema):
    class Config:
        model = Client
        model_fields = ["id", "alias", "fiscal_name", "cif", "created"]


class ClientListResponse(ModelSchema):
    class Config:
        model = Client
        model_fields = ["id", "alias", "fiscal_name", "created"]


class ClientDetailResponse(ModelSchema):
    class Config:
        model = Client
        model_fields = ["id", "alias", "fiscal_name", "cif", "created"]
