import pytest

from common.client import client
from supply_points.models import SupplyPoint

API_URL = f"/supply_points/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, supply_point):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == SupplyPoint.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_supply_point_admin_user(admin_user, supply_point_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json=supply_point_create_request)
    new_supply_point = SupplyPoint.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_supply_point.id
    assert json_response["alias"] == supply_point_create_request.alias


@pytest.mark.django_db
def test_update_supply_point_admin_user(
    admin_user, supply_point, supply_point_update_request
):
    client.set_user(admin_user)
    response = client.put(
        f"{API_URL}{supply_point.id}", json=supply_point_update_request
    )
    supply_point.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == supply_point.id
    assert json_response["alias"] == supply_point_update_request.alias


@pytest.mark.django_db
def test_partial_update_supply_point_admin_user(
    admin_user, supply_point, supply_point_update_request
):
    client.set_user(admin_user)
    response = client.patch(
        f"{API_URL}{supply_point.id}", json=supply_point_update_request
    )
    supply_point.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == supply_point.id
    assert json_response["alias"] == supply_point_update_request.alias
