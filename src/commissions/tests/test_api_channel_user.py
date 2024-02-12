import pytest
from guardian.shortcuts import assign_perm

from commissions.models import Commission
from commissions.permissions import CommissionPermissions
from common.client import client

API_URL = f"/commissions/"


@pytest.mark.django_db
def test_get_list(channel_user, commission):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list(channel_user, commission):
    client.set_user(channel_user)
    assign_perm(CommissionPermissions.READ, channel_user, commission)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_commission_not_allowed(channel_user, commission_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=commission_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_commission_allowed(channel_user, commission_create_request):
    client.set_user(channel_user)
    assign_perm(CommissionPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=commission_create_request)
    new_commission = Commission.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_commission.id
    assert json_response["name"] == commission_create_request.name


@pytest.mark.django_db
def test_update_commission_not_allowed(
    channel_user, commission, commission_update_request
):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{commission.id}", json=commission_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_commission_allowed(channel_user, commission, commission_update_request):
    client.set_user(channel_user)
    assign_perm(CommissionPermissions.EDIT, channel_user, commission)
    response = client.put(f"{API_URL}{commission.id}", json=commission_update_request)
    assert response.status_code == 200
    commission.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == commission.id
    assert json_response["name"] == commission_update_request.name


@pytest.mark.django_db
def test_partial_update_commission_not_allowed(
    channel_user, commission, commission_update_request
):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{commission.id}", json=commission_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_commission_allowed(
    channel_user, commission, commission_update_request
):
    client.set_user(channel_user)
    assign_perm(CommissionPermissions.EDIT, channel_user, commission)
    response = client.patch(f"{API_URL}{commission.id}", json=commission_update_request)
    assert response.status_code == 200
    commission.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == commission.id
    assert json_response["name"] == commission_update_request.name
