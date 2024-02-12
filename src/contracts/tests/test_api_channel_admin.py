import pytest

from common.client import client
from contracts.models import Contract

API_URL = f"/contracts/"


@pytest.mark.django_db
def test_get_list(channel_admin, contract):
    client.set_user(channel_admin)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_contract(channel_admin, contract_create_request):
    client.set_user(channel_admin)
    response = client.post(API_URL, json=contract_create_request)
    new_contract = Contract.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_contract.id


@pytest.mark.django_db
def test_update_contract(channel_admin, contract, contract_update_request):
    client.set_user(channel_admin)
    response = client.put(f"{API_URL}{contract.id}", json=contract_update_request)
    contract.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contract.id


@pytest.mark.django_db
def test_partial_update_contract(channel_admin, contract, contract_update_request):
    client.set_user(channel_admin)
    response = client.patch(f"{API_URL}{contract.id}", json=contract_update_request)
    contract.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == contract.id
