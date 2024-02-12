import pytest

from guardian.shortcuts import assign_perm
from common.client import client
from common.pagination import EMPTY_LIST_RESPONSE
from suggested_rates.models import SuggestedRate
from suggested_rates.permissions import SuggestedRatePermissions

API_URL = f"/suggested_rates/"


@pytest.mark.django_db
def test_get_list(channel_user, suggested_rate):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10

@pytest.mark.django_db
def test_get_list_no_permission(channel_user, suggested_rate):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == EMPTY_LIST_RESPONSE


@pytest.mark.django_db
def test_get_list(channel_user, suggested_rate):
    client.set_user(channel_user)
    assign_perm(SuggestedRatePermissions.READ, channel_user, suggested_rate)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_suggested_rate_not_allowed(channel_user, suggested_rate_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=suggested_rate_create_request)
    assert response.status_code == 401

@pytest.mark.django_db
def test_create_suggested_rate_allowed(channel_user, suggested_rate_create_request):
    client.set_user(channel_user)
    assign_perm(SuggestedRatePermissions.CREATE, channel_user)
    response = client.post(API_URL, json=suggested_rate_create_request)
    new_suggested_rate = SuggestedRate.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_suggested_rate.id
    assert json_response["name"] == suggested_rate_create_request.name


@pytest.mark.django_db
def test_update_suggested_rate_not_allowed(channel_user, suggested_rate, suggested_rate_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{suggested_rate.id}", json=suggested_rate_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_suggested_rate_allowed(channel_user, suggested_rate, suggested_rate_update_request):
    client.set_user(channel_user)
    assign_perm(SuggestedRatePermissions.EDIT, channel_user, suggested_rate)
    response = client.put(f"{API_URL}{suggested_rate.id}", json=suggested_rate_update_request)
    assert response.status_code == 200
    suggested_rate.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == suggested_rate.id
    assert json_response["name"] == suggested_rate_update_request.name


@pytest.mark.django_db
def test_partial_update_suggested_rate_not_allowed(channel_user, suggested_rate, suggested_rate_update_request):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{suggested_rate.id}", json=suggested_rate_update_request)
    assert response.status_code == 401

@pytest.mark.django_db
def test_partial_update_suggested_rate_allowed(channel_user, suggested_rate, suggested_rate_update_request):
    client.set_user(channel_user)
    assign_perm(SuggestedRatePermissions.EDIT, channel_user, suggested_rate)
    response = client.patch(f"{API_URL}{suggested_rate.id}", json=suggested_rate_update_request)
    assert response.status_code == 200
    suggested_rate.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == suggested_rate.id
    assert json_response["name"] == suggested_rate_update_request.name
