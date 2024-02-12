from decimal import Decimal

import pytest

from config import settings
from invoices.api.schemas.requests import InvoiceRequest, InvoiceUpdateRequest


@pytest.fixture
def invoice_create_request(channel_client):
    data = InvoiceRequest(
        channel_id=channel_client.id,
        invoice_date="2024-12-12",
        cif="12345678Z",
        base_price_amount=Decimal(10),
        base_price_currency=settings.DEFAULT_CURRENCY,
        vat_amount=Decimal(10),
        vat_currency=settings.DEFAULT_CURRENCY,
        total_amount=Decimal(10),
        total_currency=settings.DEFAULT_CURRENCY,
    )
    yield data


@pytest.fixture
def invoice_update_request(channel_client):
    data = InvoiceUpdateRequest(
        channel_id=channel_client.id,
        invoice_date="2024-12-12",
        cif="12345678Z",
        base_price_amount=Decimal(10),
        base_price_currency=settings.DEFAULT_CURRENCY,
        vat_amount=Decimal(10),
        vat_currency=settings.DEFAULT_CURRENCY,
        total_amount=Decimal(10),
        total_currency=settings.DEFAULT_CURRENCY,
    )
    yield data
