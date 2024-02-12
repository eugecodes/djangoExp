from ninja import ModelSchema

from addresses.models import Address


class AddressRequest(ModelSchema):
    channel_id: int = None

    class Config:
        model = Address
        model_fields = ["address", "postal_code", "city", "province"]
        optional_fields = ["address", "postal_code", "city", "province"]


class AddressUpdateRequest(ModelSchema):
    class Config:
        model = Address
        model_fields = ["address", "postal_code", "city", "province"]
        optional_fields = ["address", "postal_code", "city", "province"]
