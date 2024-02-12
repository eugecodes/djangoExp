import pytest

from common.client import client
from suggested_rates.models import SuggestedRate

API_URL = f"/suggested_rates/"


@pytest.mark.django_db
def test_get_list(channel_admin, suggested_rate):
    client.set_user(channel_admin)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_suggested_rate(channel_admin, suggested_rate_create_request):
    client.set_user(channel_admin)
    response = client.post(API_URL, json=suggested_rate_create_request)
    new_suggested_rate = SuggestedRate.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_suggested_rate.id
    assert json_response["name"] == suggested_rate_create_request.name


@pytest.mark.django_db
def test_update_suggested_rate(channel_admin, suggested_rate, suggested_rate_update_request):
    client.set_user(channel_admin)
    response = client.put(f"{API_URL}{suggested_rate.id}", json=suggested_rate_update_request)
    suggested_rate.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == suggested_rate.id
    assert json_response["name"] == suggested_rate_update_request.name


@pytest.mark.django_db
def test_partial_update_suggested_rate(channel_admin, suggested_rate, suggested_rate_update_request):
    client.set_user(channel_admin)
    response = client.patch(f"{API_URL}{suggested_rate.id}", json=suggested_rate_update_request)
    suggested_rate.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == suggested_rate.id
    assert json_response["name"] == suggested_rate_update_request.name
