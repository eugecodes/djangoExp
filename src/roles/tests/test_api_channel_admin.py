import pytest

from common.client import client
from roles.models import Role

API_URL = f"/roles/"


@pytest.mark.django_db
def test_get_list(channel_admin, role):
    client.set_user(channel_admin)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_role(channel_admin, role_create_request):
    client.set_user(channel_admin)
    response = client.post(API_URL, json=role_create_request)
    new_role = Role.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_role.id


@pytest.mark.django_db
def test_update_role(channel_admin, admin_channel_role, role_update_request):
    role, group = admin_channel_role
    client.set_user(channel_admin)
    response = client.put(f"{API_URL}{role.id}", json=role_update_request)
    role.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == role.id
    assert json_response["name"] == role_update_request.name


@pytest.mark.django_db
def test_partial_update_role(channel_admin, admin_channel_role, role_update_request):
    role, group = admin_channel_role
    client.set_user(channel_admin)
    response = client.patch(f"{API_URL}{role.id}", json=role_update_request)
    role.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == role.id
    assert json_response["name"] == role_update_request.name
