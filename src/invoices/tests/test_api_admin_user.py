import pytest

from common.client import client
from invoices.models import Invoice

API_URL = f"/invoices/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, invoice):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == Invoice.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_invoice_admin_user(admin_user, invoice_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json=invoice_create_request)
    new_invoice = Invoice.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_invoice.id
    assert json_response["cif"] == invoice_create_request.cif


@pytest.mark.django_db
def test_update_invoice_admin_user(admin_user, invoice, invoice_update_request):
    client.set_user(admin_user)
    response = client.put(f"{API_URL}{invoice.id}", json=invoice_update_request)
    invoice.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == invoice.id
    assert json_response["cif"] == invoice_update_request.cif


@pytest.mark.django_db
def test_partial_update_invoice_admin_user(admin_user, invoice, invoice_update_request):
    client.set_user(admin_user)
    response = client.patch(f"{API_URL}{invoice.id}", json=invoice_update_request)
    invoice.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == invoice.id
    assert json_response["cif"] == invoice_update_request.cif
