from ninja import ModelSchema

from common.api.responses import PhoneNumberSchema
from contacts.models import Contact


class BasicContactResponse(ModelSchema):
    phone: PhoneNumberSchema

    class Config:
        model = Contact
        model_fields = [
            "id",
            "name",
            "email",
            # "phone",
            "is_main_contact",
        ]
        arbitrary_types_allowed = True


class ContactListResponse(ModelSchema):
    class Config:
        model = Contact
        model_fields = [
            "id",
            "name",
        ]


class ContactDetailResponse(ModelSchema):
    phone: str

    class Config:
        model = Contact
        model_fields = [
            "id",
            "name",
            "email",
            # "phone",
            "is_main_contact",
        ]
        arbitrary_types_allowed = True
