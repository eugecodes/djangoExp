from ninja import ModelSchema

from marketers.models import Marketer


class MarketerRequest(ModelSchema):
    address_id: int

    class Config:
        model = Marketer
        model_fields = ["name", "fiscal_name", "cif", "email", "fee", "max_consume"]
        fields_optional = ["email", "fee", "max_consume"]
