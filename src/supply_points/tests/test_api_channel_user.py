import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from common.pagination import EMPTY_LIST_RESPONSE
from supply_points.models import SupplyPoint
from supply_points.permissions import SupplyPointPermissions

API_URL = f"/supply_points/"


@pytest.mark.django_db
def test_get_list(channel_user, supply_point):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list_no_permission(channel_user, supply_point):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == EMPTY_LIST_RESPONSE


@pytest.mark.django_db
def test_get_list(channel_user, supply_point):
    client.set_user(channel_user)
    assign_perm(SupplyPointPermissions.READ, channel_user, supply_point)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_supply_point_not_allowed(channel_user, supply_point_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=supply_point_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_supply_point_allowed(channel_user, supply_point_create_request):
    client.set_user(channel_user)
    assign_perm(SupplyPointPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=supply_point_create_request)
    new_supply_point = SupplyPoint.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_supply_point.id
    assert json_response["alias"] == supply_point_create_request.alias


@pytest.mark.django_db
def test_update_supply_point_not_allowed(
    channel_user, supply_point, supply_point_update_request
):
    client.set_user(channel_user)
    response = client.put(
        f"{API_URL}{supply_point.id}", json=supply_point_update_request
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_supply_point_allowed(
    channel_user, supply_point, supply_point_update_request
):
    client.set_user(channel_user)
    assign_perm(SupplyPointPermissions.EDIT, channel_user, supply_point)
    response = client.put(
        f"{API_URL}{supply_point.id}", json=supply_point_update_request
    )
    assert response.status_code == 200
    supply_point.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == supply_point.id
    assert json_response["alias"] == supply_point_update_request.alias


@pytest.mark.django_db
def test_partial_update_supply_point_not_allowed(
    channel_user, supply_point, supply_point_update_request
):
    client.set_user(channel_user)
    response = client.patch(
        f"{API_URL}{supply_point.id}", json=supply_point_update_request
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_supply_point_allowed(
    channel_user, supply_point, supply_point_update_request
):
    client.set_user(channel_user)
    assign_perm(SupplyPointPermissions.EDIT, channel_user, supply_point)
    response = client.patch(
        f"{API_URL}{supply_point.id}", json=supply_point_update_request
    )
    assert response.status_code == 200
    supply_point.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == supply_point.id
    assert json_response["alias"] == supply_point_update_request.alias
