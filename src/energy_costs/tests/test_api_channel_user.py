import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from energy_costs.models import EnergyCost
from energy_costs.permissions import EnergyCostPermissions

API_URL = f"/energy_costs/"


@pytest.mark.django_db
def test_get_list(channel_user, energy_cost):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list(channel_user, energy_cost):
    client.set_user(channel_user)
    assign_perm(EnergyCostPermissions.READ, channel_user, energy_cost)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == EnergyCost.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_energy_cost_not_allowed(channel_user, energy_cost_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=energy_cost_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_energy_cost_allowed(channel_user, energy_cost_create_request):
    client.set_user(channel_user)
    assign_perm(EnergyCostPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=energy_cost_create_request)
    new_energy_cost = EnergyCost.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_energy_cost.id
    assert json_response["code"] == energy_cost_create_request.code


@pytest.mark.django_db
def test_update_energy_cost_not_allowed(
    channel_user, energy_cost, energy_cost_update_request
):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{energy_cost.id}", json=energy_cost_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_energy_cost_allowed(
    channel_user, energy_cost, energy_cost_update_request
):
    client.set_user(channel_user)
    assign_perm(EnergyCostPermissions.EDIT, channel_user, energy_cost)
    response = client.put(f"{API_URL}{energy_cost.id}", json=energy_cost_update_request)
    assert response.status_code == 200
    energy_cost.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == energy_cost.id
    assert json_response["code"] == energy_cost_update_request.code


@pytest.mark.django_db
def test_partial_update_energy_cost_not_allowed(
    channel_user, energy_cost, energy_cost_update_request
):
    client.set_user(channel_user)
    response = client.patch(
        f"{API_URL}{energy_cost.id}", json=energy_cost_update_request
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_energy_cost_allowed(
    channel_user, energy_cost, energy_cost_update_request
):
    client.set_user(channel_user)
    assign_perm(EnergyCostPermissions.EDIT, channel_user, energy_cost)
    response = client.patch(
        f"{API_URL}{energy_cost.id}", json=energy_cost_update_request
    )
    assert response.status_code == 200
    energy_cost.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == energy_cost.id
    assert json_response["code"] == energy_cost_update_request.code
