import pytest
from guardian.shortcuts import assign_perm

from addresses.models import Address
from addresses.permissions import AddressPermissions
from common.client import client
from common.pagination import EMPTY_LIST_RESPONSE

API_URL = f"/addresses/"


@pytest.mark.django_db
def test_get_list(channel_user, address):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list_no_permission(channel_user, address):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == EMPTY_LIST_RESPONSE


@pytest.mark.django_db
def test_get_list(channel_user, address):
    client.set_user(channel_user)
    assign_perm(AddressPermissions.READ, channel_user, address)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_address_not_allowed(channel_user, address_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=address_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_address_allowed(channel_user, address_create_request):
    client.set_user(channel_user)
    assign_perm(AddressPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=address_create_request)
    new_address = Address.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_address.id
    assert json_response["address"] == address_create_request.address


@pytest.mark.django_db
def test_update_address_not_allowed(channel_user, address, address_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{address.id}", json=address_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_address_allowed(channel_user, address, address_update_request):
    client.set_user(channel_user)
    assign_perm(AddressPermissions.EDIT, channel_user, address)
    response = client.put(f"{API_URL}{address.id}", json=address_update_request)
    assert response.status_code == 200
    address.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == address.id
    assert json_response["address"] == address_update_request.address


@pytest.mark.django_db
def test_partial_update_address_not_allowed(
    channel_user, address, address_update_request
):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{address.id}", json=address_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_address_allowed(channel_user, address, address_update_request):
    client.set_user(channel_user)
    assign_perm(AddressPermissions.EDIT, channel_user, address)
    response = client.patch(f"{API_URL}{address.id}", json=address_update_request)
    assert response.status_code == 200
    address.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == address.id
    assert json_response["address"] == address_update_request.address
