from ninja import ModelSchema

from common.api.responses import MoneySchema
from invoices.models import Invoice


class BasicInvoiceResponse(ModelSchema):
    base_price: MoneySchema
    vat: MoneySchema
    total: MoneySchema

    class Config:
        model = Invoice
        model_fields = [
            "id",
            "created",
            "channel",
            "invoice_date",
            "cif",
        ]


class InvoiceListResponse(ModelSchema):
    total: MoneySchema

    class Config:
        model = Invoice
        model_fields = ["id", "invoice_date"]


class InvoiceDetailResponse(ModelSchema):
    base_price: MoneySchema
    vat: MoneySchema
    total: MoneySchema

    class Config:
        model = Invoice
        model_fields = [
            "id",
            "created",
            "channel",
            "invoice_date",
            "cif",
        ]
