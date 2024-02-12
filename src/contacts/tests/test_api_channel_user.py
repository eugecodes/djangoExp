import pytest

from guardian.shortcuts import assign_perm
from common.client import client
from common.pagination import EMPTY_LIST_RESPONSE
from contacts.models import Contact
from contacts.permissions import ContactPermissions

API_URL = f"/contacts/"


@pytest.mark.django_db
def test_get_list(channel_user, contact):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10

@pytest.mark.django_db
def test_get_list_no_permission(channel_user, contact):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == EMPTY_LIST_RESPONSE


@pytest.mark.django_db
def test_get_list(channel_user, contact):
    client.set_user(channel_user)
    assign_perm(ContactPermissions.READ, channel_user, contact)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_contact_not_allowed(channel_user, contact_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=contact_create_request)
    assert response.status_code == 401

@pytest.mark.django_db
def test_create_contact_allowed(channel_user, contact_create_request):
    client.set_user(channel_user)
    assign_perm(ContactPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=contact_create_request)
    new_contact = Contact.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_contact.id
    assert json_response["name"] == contact_create_request.name


@pytest.mark.django_db
def test_update_contact_not_allowed(channel_user, contact, contact_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{contact.id}", json=contact_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_contact_allowed(channel_user, contact, contact_update_request):
    client.set_user(channel_user)
    assign_perm(ContactPermissions.EDIT, channel_user, contact)
    response = client.put(f"{API_URL}{contact.id}", json=contact_update_request)
    assert response.status_code == 200
    contact.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contact.id
    assert json_response["name"] == contact_update_request.name


@pytest.mark.django_db
def test_partial_update_contact_not_allowed(channel_user, contact, contact_update_request):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{contact.id}", json=contact_update_request)
    assert response.status_code == 401

@pytest.mark.django_db
def test_partial_update_contact_allowed(channel_user, contact, contact_update_request):
    client.set_user(channel_user)
    assign_perm(ContactPermissions.EDIT, channel_user, contact)
    response = client.patch(f"{API_URL}{contact.id}", json=contact_update_request)
    assert response.status_code == 200
    contact.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contact.id
    assert json_response["name"] == contact_update_request.name
