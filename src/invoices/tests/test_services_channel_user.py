import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from invoices.permissions import InvoicePermissions
from invoices.services import (
    invoice_create,
    invoice_update,
)


@pytest.mark.django_db
def test_create_invoice_channel_user_not_allowed(channel_user, invoice_create_request):
    with pytest.raises(AuthenticationError):
        invoice_create(invoice_create_request, channel_user)


@pytest.mark.django_db
def test_create_invoice_channel_user_allowed(channel_user, invoice_create_request):
    assign_perm(InvoicePermissions.CREATE, channel_user)
    new_invoice = invoice_create(invoice_create_request, channel_user)
    assert new_invoice.cif == invoice_create_request.cif


@pytest.mark.django_db
def test_update_invoice_channel_user_not_allowed(
    channel_user, invoice, invoice_update_request
):
    with pytest.raises(AuthenticationError):
        invoice_update(invoice, invoice_update_request, channel_user)


@pytest.mark.django_db
def test_update_invoice_channel_user_allowed(
    channel_user, invoice, invoice_update_request
):
    assign_perm(InvoicePermissions.EDIT, channel_user, invoice)
    updatable_invoice = invoice_update(invoice, invoice_update_request, channel_user)
    assert updatable_invoice.cif == invoice_update_request.cif
