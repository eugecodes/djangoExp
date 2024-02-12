import pytest
from guardian.shortcuts import assign_perm

from clients.models import Client
from clients.permissions import ClientPermissions
from common.client import client
from common.pagination import EMPTY_LIST_RESPONSE

API_URL = f"/clients/"


@pytest.mark.django_db
def test_get_list_no_permission(channel_user, channel_client):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == EMPTY_LIST_RESPONSE


@pytest.mark.django_db
def test_get_list(channel_user, channel_client):
    client.set_user(channel_user)
    assign_perm(ClientPermissions.READ, channel_user, channel_client)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_client_not_allowed(channel_user, client_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=client_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_client_allowed(channel_user, client_create_request):
    client.set_user(channel_user)
    assign_perm(ClientPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=client_create_request)
    new_client = Client.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_client.id
    assert json_response["alias"] == client_create_request.alias
    assert json_response["fiscal_name"] == client_create_request.fiscal_name
    assert json_response["cif"] == client_create_request.cif


@pytest.mark.django_db
def test_update_client_not_allowed(channel_user, channel_client, client_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{channel_client.id}", json=client_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_client_allowed(channel_user, channel_client, client_update_request):
    client.set_user(channel_user)
    assign_perm(ClientPermissions.EDIT, channel_user, channel_client)
    response = client.put(f"{API_URL}{channel_client.id}", json=client_update_request)
    assert response.status_code == 200
    channel_client.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == channel_client.id
    assert json_response["alias"] == client_update_request.alias
    assert json_response["fiscal_name"] == client_update_request.fiscal_name
    assert json_response["cif"] == client_update_request.cif


@pytest.mark.django_db
def test_partial_update_client_not_allowed(
    channel_user, channel_client, client_update_request
):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{channel_client.id}", json=client_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_client_allowed(
    channel_user, channel_client, client_update_request
):
    client.set_user(channel_user)
    assign_perm(ClientPermissions.EDIT, channel_user, channel_client)
    response = client.patch(f"{API_URL}{channel_client.id}", json=client_update_request)
    assert response.status_code == 200
    channel_client.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == channel_client.id
    assert json_response["alias"] == client_update_request.alias
    assert json_response["fiscal_name"] == client_update_request.fiscal_name
    assert json_response["cif"] == client_update_request.cif
