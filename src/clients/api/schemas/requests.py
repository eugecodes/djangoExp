from ninja import ModelSchema

from clients.models import Client


class ClientRequest(ModelSchema):
    channel_id: int = None

    class Config:
        model = Client
        model_fields = [
            "alias",
            "fiscal_name",
            "cif",
            "client_type",
            "invoice_notification_type",
            "invoice_email",
            "invoice_postal",
            "is_renewable",
        ]
        fields_optional = [
            "channel_id",
            "invoice_email",
            "invoice_postal",
            "is_renewable",
        ]


class ClientUpdateRequest(ModelSchema):
    class Config:
        model = Client
        model_fields = [
            "alias",
            "fiscal_name",
            "cif",
            "client_type",
            "invoice_notification_type",
            "invoice_email",
            "invoice_postal",
            "is_renewable",
        ]
        fields_optional = [
            "alias",
            "fiscal_name",
            "cif",
            "client_type",
            "invoice_notification_type",
            "invoice_email",
            "invoice_postal",
            "is_renewable",
        ]
