import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from margins.models import Margin
from margins.permissions import MarginPermissions

API_URL = f"/margins/"


@pytest.mark.django_db
def test_get_list(channel_user, margin):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list(channel_user, margin):
    client.set_user(channel_user)
    assign_perm(MarginPermissions.READ, channel_user, margin)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_margin_not_allowed(channel_user, margin_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=margin_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_margin_allowed(channel_user, margin_create_request):
    client.set_user(channel_user)
    assign_perm(MarginPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=margin_create_request)
    new_margin = Margin.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_margin.id
    assert json_response["type"] == margin_create_request.type


@pytest.mark.django_db
def test_update_margin_not_allowed(channel_user, margin, margin_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{margin.id}", json=margin_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_margin_allowed(channel_user, margin, margin_update_request):
    client.set_user(channel_user)
    assign_perm(MarginPermissions.EDIT, channel_user, margin)
    response = client.put(f"{API_URL}{margin.id}", json=margin_update_request)
    assert response.status_code == 200
    margin.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == margin.id


@pytest.mark.django_db
def test_partial_update_margin_not_allowed(channel_user, margin, margin_update_request):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{margin.id}", json=margin_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_margin_allowed(channel_user, margin, margin_update_request):
    client.set_user(channel_user)
    assign_perm(MarginPermissions.EDIT, channel_user, margin)
    response = client.patch(f"{API_URL}{margin.id}", json=margin_update_request)
    assert response.status_code == 200
    margin.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == margin.id
