from ninja import ModelSchema

from addresses.models import Address


class BasicAddressResponse(ModelSchema):
    class Config:
        model = Address
        model_fields = ["id", "address", "postal_code", "city", "province"]


class AddressListResponse(ModelSchema):
    class Config:
        model = Address
        model_fields = ["id", "address"]


class AddressDetailResponse(ModelSchema):
    class Config:
        model = Address
        model_fields = ["id", "created", "address", "postal_code", "city", "province"]
