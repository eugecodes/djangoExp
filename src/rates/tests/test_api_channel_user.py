import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from rates.permissions import RatePermissions

API_URL = f"/rates/"


@pytest.mark.django_db
def test_get_list(channel_user, rate):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list(channel_user, rate):
    client.set_user(channel_user)
    assign_perm(RatePermissions.READ, channel_user, rate)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_rate_not_allowed(channel_user, rate_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=rate_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_rate_not_allowed(channel_user, rate, rate_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{rate.id}", json=rate_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_rate_not_allowed(channel_user, rate, rate_update_request):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{rate.id}", json=rate_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_rate_allowed(channel_user, rate, rate_update_request):
    client.set_user(channel_user)
    assign_perm(RatePermissions.EDIT, channel_user, rate)
    response = client.patch(f"{API_URL}{rate.id}", json=rate_update_request)
    assert response.status_code == 200
    rate.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == rate.id
