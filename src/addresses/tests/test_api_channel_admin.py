import pytest

from addresses.models import Address
from common.client import client

API_URL = f"/addresses/"


@pytest.mark.django_db
def test_get_list(channel_admin, address):
    client.set_user(channel_admin)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_address(channel_admin, address_create_request):
    client.set_user(channel_admin)
    response = client.post(API_URL, json=address_create_request)
    new_address = Address.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_address.id
    assert json_response["address"] == address_create_request.address


@pytest.mark.django_db
def test_update_address(channel_admin, address, address_update_request):
    client.set_user(channel_admin)
    response = client.put(f"{API_URL}{address.id}", json=address_update_request)
    address.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == address.id
    assert json_response["address"] == address_update_request.address


@pytest.mark.django_db
def test_partial_update_address(channel_admin, address, address_update_request):
    client.set_user(channel_admin)
    response = client.patch(f"{API_URL}{address.id}", json=address_update_request)
    address.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == address.id
    assert json_response["address"] == address_update_request.address
