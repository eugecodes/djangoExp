import pytest

from common.client import client

API_URL = f"/roles/"


@pytest.mark.django_db
def test_get_list(channel_user, role):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_role_now_allowed(channel_user, role_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=role_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_role(channel_user, user_channel_role, role_update_request):
    client.set_user(channel_user)
    role, group = user_channel_role
    response = client.put(f"{API_URL}{role.id}", json=role_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_role(channel_user, user_channel_role, role_update_request):
    client.set_user(channel_user)
    role, group = user_channel_role
    response = client.patch(f"{API_URL}{role.id}", json=role_update_request)
    assert response.status_code == 401
