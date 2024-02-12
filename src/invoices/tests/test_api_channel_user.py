import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from common.pagination import EMPTY_LIST_RESPONSE
from invoices.models import Invoice
from invoices.permissions import InvoicePermissions

API_URL = f"/invoices/"


@pytest.mark.django_db
def test_get_list(channel_user, invoice):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list_no_permission(channel_user, invoice):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == EMPTY_LIST_RESPONSE


@pytest.mark.django_db
def test_get_list(channel_user, invoice):
    client.set_user(channel_user)
    assign_perm(InvoicePermissions.READ, channel_user, invoice)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_invoice_not_allowed(channel_user, invoice_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=invoice_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_invoice_allowed(channel_user, invoice_create_request):
    client.set_user(channel_user)
    assign_perm(InvoicePermissions.CREATE, channel_user)
    response = client.post(API_URL, json=invoice_create_request)
    new_invoice = Invoice.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_invoice.id
    assert json_response["cif"] == invoice_create_request.cif


@pytest.mark.django_db
def test_update_invoice_not_allowed(channel_user, invoice, invoice_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{invoice.id}", json=invoice_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_invoice_allowed(channel_user, invoice, invoice_update_request):
    client.set_user(channel_user)
    assign_perm(InvoicePermissions.EDIT, channel_user, invoice)
    response = client.put(f"{API_URL}{invoice.id}", json=invoice_update_request)
    assert response.status_code == 200
    invoice.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == invoice.id
    assert json_response["cif"] == invoice_update_request.cif


@pytest.mark.django_db
def test_partial_update_invoice_not_allowed(
    channel_user, invoice, invoice_update_request
):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{invoice.id}", json=invoice_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_invoice_allowed(channel_user, invoice, invoice_update_request):
    client.set_user(channel_user)
    assign_perm(InvoicePermissions.EDIT, channel_user, invoice)
    response = client.patch(f"{API_URL}{invoice.id}", json=invoice_update_request)
    assert response.status_code == 200
    invoice.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == invoice.id
    assert json_response["cif"] == invoice_update_request.cif
