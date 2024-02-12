import pytest

from invoices.services import (
    invoice_create,
    invoice_update,
)


@pytest.mark.django_db
def test_create_invoice_admin_user(admin_user, invoice_create_request):
    new_invoice = invoice_create(invoice_create_request, admin_user)
    assert new_invoice.cif == invoice_create_request.cif


@pytest.mark.django_db
def test_update_invoice_admin_user(admin_user, invoice, invoice_update_request):
    updatable_invoice = invoice_update(invoice, invoice_update_request, admin_user)
    assert updatable_invoice.cif == invoice_update_request.cif
