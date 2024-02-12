import pytest

from common.client import client
from energy_costs.models import EnergyCost

API_URL = f"/energy_costs/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, energy_cost):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == EnergyCost.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_energy_cost_admin_user(admin_user, energy_cost_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json=energy_cost_create_request)
    new_energy_cost = EnergyCost.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_energy_cost.id
    assert json_response["code"] == energy_cost_create_request.code


@pytest.mark.django_db
def test_update_energy_cost_admin_user(
    admin_user, energy_cost, energy_cost_update_request
):
    client.set_user(admin_user)
    response = client.put(f"{API_URL}{energy_cost.id}", json=energy_cost_update_request)
    energy_cost.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == energy_cost.id
    assert json_response["code"] == energy_cost_update_request.code


@pytest.mark.django_db
def test_partial_update_energy_cost_admin_user(
    admin_user, energy_cost, energy_cost_update_request
):
    client.set_user(admin_user)
    response = client.patch(
        f"{API_URL}{energy_cost.id}", json=energy_cost_update_request
    )
    energy_cost.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == energy_cost.id
    assert json_response["code"] == energy_cost_update_request.code
