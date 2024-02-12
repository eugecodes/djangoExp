import pytest

from common.client import client
from commissions.models import Commission

API_URL = f"/commissions/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, commission):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == Commission.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_commission_admin_user(admin_user, commission_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json=commission_create_request)
    new_commission = Commission.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_commission.id
    assert json_response["name"] == commission_create_request.name


@pytest.mark.django_db
def test_update_commission_admin_user(admin_user, commission, commission_update_request):
    client.set_user(admin_user)
    response = client.put(f"{API_URL}{commission.id}", json=commission_update_request)
    commission.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == commission.id
    assert json_response["name"] == commission_update_request.name


@pytest.mark.django_db
def test_partial_update_commission_admin_user(admin_user, commission, commission_update_request):
    client.set_user(admin_user)
    response = client.patch(f"{API_URL}{commission.id}", json=commission_update_request)
    commission.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == commission.id
    assert json_response["name"] == commission_update_request.name
