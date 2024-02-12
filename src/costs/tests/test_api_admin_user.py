import pytest

from common.client import client
from costs.models import OtherCost

API_URL = f"/costs/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, cost):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == OtherCost.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_cost_admin_user(admin_user, cost_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json=cost_create_request)
    new_cost = OtherCost.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_cost.id
    assert json_response["name"] == cost_create_request.name


@pytest.mark.django_db
def test_update_cost_admin_user(admin_user, cost, cost_update_request):
    client.set_user(admin_user)
    response = client.put(f"{API_URL}{cost.id}", json=cost_update_request)
    cost.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == cost.id
    assert json_response["name"] == cost_update_request.name


@pytest.mark.django_db
def test_partial_update_cost_admin_user(admin_user, cost, cost_update_request):
    client.set_user(admin_user)
    response = client.patch(f"{API_URL}{cost.id}", json=cost_update_request)
    cost.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == cost.id
    assert json_response["name"] == cost_update_request.name
