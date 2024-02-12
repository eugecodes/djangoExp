import pytest

from common.client import client
from contacts.models import Contact

API_URL = f"/contacts/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, contact):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == Contact.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_contact_admin_user(admin_user, contact_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json=contact_create_request)
    new_contact = Contact.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_contact.id
    assert json_response["name"] == contact_create_request.name


@pytest.mark.django_db
def test_update_contact_admin_user(admin_user, contact, contact_update_request):
    client.set_user(admin_user)
    response = client.put(f"{API_URL}{contact.id}", json=contact_update_request)
    contact.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contact.id
    assert json_response["name"] == contact_update_request.name


@pytest.mark.django_db
def test_partial_update_contact_admin_user(admin_user, contact, contact_update_request):
    client.set_user(admin_user)
    response = client.patch(f"{API_URL}{contact.id}", json=contact_update_request)
    contact.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contact.id
    assert json_response["name"] == contact_update_request.name
