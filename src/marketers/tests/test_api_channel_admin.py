import pytest

from common.client import client

API_URL = f"/marketers/"


@pytest.mark.django_db
def test_get_list(channel_admin, marketer):
    client.set_user(channel_admin)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_marketer(channel_admin, marketer_create_request):
    client.set_user(channel_admin)
    response = client.post(API_URL, json=marketer_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_marketer(channel_admin, marketer, marketer_update_request):
    client.set_user(channel_admin)
    response = client.put(f"{API_URL}{marketer.id}", json=marketer_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_marketer(channel_admin, marketer, marketer_update_request):
    client.set_user(channel_admin)
    response = client.patch(f"{API_URL}{marketer.id}", json=marketer_update_request)
    assert response.status_code == 401
