import pytest

from common.client import client
from contacts.models import Contact

API_URL = f"/contacts/"


@pytest.mark.django_db
def test_get_list(channel_admin, contact):
    client.set_user(channel_admin)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_contact(channel_admin, contact_create_request):
    client.set_user(channel_admin)
    response = client.post(API_URL, json=contact_create_request)
    new_contact = Contact.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_contact.id
    assert json_response["name"] == contact_create_request.name


@pytest.mark.django_db
def test_update_contact(channel_admin, contact, contact_update_request):
    client.set_user(channel_admin)
    response = client.put(f"{API_URL}{contact.id}", json=contact_update_request)
    contact.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contact.id
    assert json_response["name"] == contact_update_request.name


@pytest.mark.django_db
def test_partial_update_contact(channel_admin, contact, contact_update_request):
    client.set_user(channel_admin)
    response = client.patch(f"{API_URL}{contact.id}", json=contact_update_request)
    contact.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contact.id
    assert json_response["name"] == contact_update_request.name
