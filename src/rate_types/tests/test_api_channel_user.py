import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from rate_types.models import RateType
from rate_types.permissions import RateTypePermissions

API_URL = f"/rate_types/"


@pytest.mark.django_db
def test_get_list(channel_user, rate_type):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list(channel_user, rate_type):
    client.set_user(channel_user)
    assign_perm(RateTypePermissions.READ, channel_user, rate_type)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_rate_type_not_allowed(channel_user, rate_type_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=rate_type_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_rate_type_allowed(channel_user, rate_type_create_request):
    client.set_user(channel_user)
    assign_perm(RateTypePermissions.CREATE, channel_user)
    response = client.post(API_URL, json=rate_type_create_request)
    new_rate_type = RateType.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_rate_type.id
    assert json_response["name"] == rate_type_create_request.name


@pytest.mark.django_db
def test_update_rate_type_not_allowed(
    channel_user, rate_type, rate_type_update_request
):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{rate_type.id}", json=rate_type_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_rate_type_allowed(channel_user, rate_type, rate_type_update_request):
    client.set_user(channel_user)
    assign_perm(RateTypePermissions.EDIT, channel_user, rate_type)
    response = client.put(f"{API_URL}{rate_type.id}", json=rate_type_update_request)
    assert response.status_code == 200
    rate_type.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == rate_type.id
    assert json_response["name"] == rate_type_update_request.name


@pytest.mark.django_db
def test_partial_update_rate_type_not_allowed(
    channel_user, rate_type, rate_type_update_request
):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{rate_type.id}", json=rate_type_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_rate_type_allowed(
    channel_user, rate_type, rate_type_update_request
):
    client.set_user(channel_user)
    assign_perm(RateTypePermissions.EDIT, channel_user, rate_type)
    response = client.patch(f"{API_URL}{rate_type.id}", json=rate_type_update_request)
    assert response.status_code == 200
    rate_type.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == rate_type.id
    assert json_response["name"] == rate_type_update_request.name
