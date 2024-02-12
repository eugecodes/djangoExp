import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from common.pagination import EMPTY_LIST_RESPONSE
from contracts.models import Contract
from contracts.permissions import ContractPermissions

API_URL = f"/contracts/"


@pytest.mark.django_db
def test_get_list(channel_user, contract):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list_no_permission(channel_user, contract):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == EMPTY_LIST_RESPONSE


@pytest.mark.django_db
def test_get_list(channel_user, contract):
    client.set_user(channel_user)
    assign_perm(ContractPermissions.READ, channel_user, contract)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_contract_not_allowed(channel_user, contract_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=contract_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_contract_allowed(channel_user, contract_create_request):
    client.set_user(channel_user)
    assign_perm(ContractPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=contract_create_request)
    new_contract = Contract.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_contract.id


@pytest.mark.django_db
def test_update_contract_not_allowed(channel_user, contract, contract_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{contract.id}", json=contract_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_contract_allowed(channel_user, contract, contract_update_request):
    client.set_user(channel_user)
    assign_perm(ContractPermissions.EDIT, channel_user, contract)
    response = client.put(f"{API_URL}{contract.id}", json=contract_update_request)
    assert response.status_code == 200
    contract.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contract.id


@pytest.mark.django_db
def test_partial_update_contract_not_allowed(
    channel_user, contract, contract_update_request
):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{contract.id}", json=contract_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_contract_allowed(
    channel_user, contract, contract_update_request
):
    client.set_user(channel_user)
    assign_perm(ContractPermissions.EDIT, channel_user, contract)
    response = client.patch(f"{API_URL}{contract.id}", json=contract_update_request)
    assert response.status_code == 200
    contract.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contract.id
