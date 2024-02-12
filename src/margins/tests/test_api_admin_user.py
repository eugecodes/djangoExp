import pytest

from common.client import client
from margins.models import Margin

API_URL = f"/margins/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, margin):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == Margin.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_margin_admin_user(admin_user, margin_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json=margin_create_request)
    new_margin = Margin.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_margin.id


@pytest.mark.django_db
def test_update_margin_admin_user(admin_user, margin, margin_update_request):
    client.set_user(admin_user)
    response = client.put(f"{API_URL}{margin.id}", json=margin_update_request)
    margin.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == margin.id
    assert json_response["type"] == margin_update_request.type


@pytest.mark.django_db
def test_partial_update_margin_admin_user(admin_user, margin, margin_update_request):
    client.set_user(admin_user)
    response = client.patch(f"{API_URL}{margin.id}", json=margin_update_request)
    margin.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == margin.id
    assert json_response["type"] == margin_update_request.type
