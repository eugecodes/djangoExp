import pytest

from common.client import client
from rates.models import Rate

API_URL = f"/rates/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, rate):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == Rate.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_rate_admin_user(admin_user, rate_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json=rate_create_request)
    new_rate = Rate.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_rate.id
    assert json_response["name"] == rate_create_request.name


@pytest.mark.django_db
def test_update_rate_admin_user(admin_user, rate, rate_update_request):
    client.set_user(admin_user)
    response = client.put(f"{API_URL}{rate.id}", json=rate_update_request)
    rate.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == rate.id
    assert json_response["name"] == rate_update_request.name


@pytest.mark.django_db
def test_partial_update_rate_admin_user(admin_user, rate, rate_update_request):
    client.set_user(admin_user)
    response = client.patch(f"{API_URL}{rate.id}", json=rate_update_request)
    rate.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == rate.id
    assert json_response["name"] == rate_update_request.name
