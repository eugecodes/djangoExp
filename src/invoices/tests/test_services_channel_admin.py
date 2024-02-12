import pytest

from invoices.services import (
    invoice_create,
    invoice_update,
)


@pytest.mark.django_db
def test_create_invoice_channel_admin(channel_admin, invoice_create_request):
    new_invoice = invoice_create(invoice_create_request, channel_admin)
    assert new_invoice.cif == invoice_create_request.cif


@pytest.mark.django_db
def test_update_invoice_channel_admin(channel_admin, invoice, invoice_update_request):
    updatable_invoice = invoice_update(invoice, invoice_update_request, channel_admin)
    assert updatable_invoice.cif == invoice_update_request.cif
