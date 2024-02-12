from ninja import ModelSchema

from marketers.models import Marketer


class BasicMarketerResponse(ModelSchema):
    class Config:
        model = Marketer
        model_fields = [
            "id",
            "created",
            "name",
            "fiscal_name",
            "cif",
            "email",
            "fee",
            "max_consume",
        ]


class MarketerListResponse(ModelSchema):
    class Config:
        model = Marketer
        model_fields = [
            "id",
            "name",
            "fiscal_name",
        ]


class MarketerDetailResponse(ModelSchema):
    class Config:
        model = Marketer
        model_fields = [
            "id",
            "created",
            "name",
            "fiscal_name",
            "cif",
            "email",
            "fee",
            "max_consume",
        ]
