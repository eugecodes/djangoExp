import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from costs.models import OtherCost
from costs.permissions import OtherCostPermissions

API_URL = f"/costs/"


@pytest.mark.django_db
def test_get_list(channel_user, cost):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list(channel_user, cost):
    client.set_user(channel_user)
    assign_perm(OtherCostPermissions.READ, channel_user, cost)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_cost_not_allowed(channel_user, cost_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=cost_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_cost_allowed(channel_user, cost_create_request):
    client.set_user(channel_user)
    assign_perm(OtherCostPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=cost_create_request)
    new_cost = OtherCost.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_cost.id
    assert json_response["name"] == cost_create_request.name


@pytest.mark.django_db
def test_update_cost_not_allowed(channel_user, cost, cost_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{cost.id}", json=cost_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_cost_allowed(channel_user, cost, cost_update_request):
    client.set_user(channel_user)
    assign_perm(OtherCostPermissions.EDIT, channel_user, cost)
    response = client.put(f"{API_URL}{cost.id}", json=cost_update_request)
    assert response.status_code == 200
    cost.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == cost.id
    assert json_response["name"] == cost_update_request.name


@pytest.mark.django_db
def test_partial_update_cost_not_allowed(channel_user, cost, cost_update_request):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{cost.id}", json=cost_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_cost_allowed(channel_user, cost, cost_update_request):
    client.set_user(channel_user)
    assign_perm(OtherCostPermissions.EDIT, channel_user, cost)
    response = client.patch(f"{API_URL}{cost.id}", json=cost_update_request)
    assert response.status_code == 200
    cost.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == cost.id
    assert json_response["name"] == cost_update_request.name
