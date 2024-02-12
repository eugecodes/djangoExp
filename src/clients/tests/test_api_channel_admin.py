import pytest

from clients.models import Client
from common.client import client

API_URL = f"/clients/"


@pytest.mark.django_db
def test_get_list(channel_admin, channel_client):
    client.set_user(channel_admin)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_client(channel_admin, client_create_request):
    client.set_user(channel_admin)
    response = client.post(API_URL, json=client_create_request)
    new_client = Client.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_client.id
    assert json_response["alias"] == client_create_request.alias
    assert json_response["fiscal_name"] == client_create_request.fiscal_name
    assert json_response["cif"] == client_create_request.cif


@pytest.mark.django_db
def test_update_client(channel_admin, channel_client, client_update_request):
    client.set_user(channel_admin)
    response = client.put(f"{API_URL}{channel_client.id}", json=client_update_request)
    channel_client.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == channel_client.id
    assert json_response["alias"] == client_update_request.alias
    assert json_response["fiscal_name"] == client_update_request.fiscal_name
    assert json_response["cif"] == client_update_request.cif


@pytest.mark.django_db
def test_partial_update_client(channel_admin, channel_client, client_update_request):
    client.set_user(channel_admin)
    response = client.patch(f"{API_URL}{channel_client.id}", json=client_update_request)
    channel_client.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == channel_client.id
    assert json_response["alias"] == client_update_request.alias
    assert json_response["fiscal_name"] == client_update_request.fiscal_name
    assert json_response["cif"] == client_update_request.cif
