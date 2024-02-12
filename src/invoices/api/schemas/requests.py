from decimal import Decimal

from djmoney.money import Money
from ninja import ModelSchema

from invoices.models import Invoice


class InvoiceRequest(ModelSchema):
    channel_id: int
    base_price: Money = None
    base_price_amount: Decimal
    base_price_currency: str
    vat: Money = None
    vat_amount: Decimal
    vat_currency: str
    total: Money = None

    class Config:
        model = Invoice
        model_fields = [
            "invoice_date",
            "cif",
        ]
        optional_fields = []
        arbitrary_types_allowed = True


class InvoiceUpdateRequest(ModelSchema):
    base_price: Money = None
    base_price_amount: Decimal
    base_price_currency: str
    vat: Money = None
    vat_amount: Decimal
    vat_currency: str
    total: Money = None

    class Config:
        model = Invoice
        model_fields = [
            "invoice_date",
            "cif",
        ]
        optional_fields = []
        arbitrary_types_allowed = True
