from ninja import ModelSchema

from contacts.models import Contact


class ContactRequest(ModelSchema):
    client_id: int

    class Config:
        model = Contact
        model_fields = [
            "name",
            "email",
            "phone",
            "is_main_contact",
        ]
        optional_fields = []


class ContactUpdateRequest(ModelSchema):
    class Config:
        model = Contact
        model_fields = [
            "name",
            "email",
            "phone",
            "is_main_contact",
        ]
        optional_fields = []
