import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from marketers.models import Marketer
from marketers.permissions import MarketerPermissions

API_URL = f"/marketers/"


@pytest.mark.django_db
def test_get_list(channel_user, marketer):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list(channel_user, marketer):
    client.set_user(channel_user)
    assign_perm(MarketerPermissions.READ, channel_user, marketer)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_marketer_not_allowed(channel_user, marketer_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=marketer_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_marketer_allowed(channel_user, marketer_create_request):
    client.set_user(channel_user)
    assign_perm(MarketerPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=marketer_create_request)
    new_marketer = Marketer.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_marketer.id
    assert json_response["name"] == marketer_create_request.name


@pytest.mark.django_db
def test_update_marketer_not_allowed(channel_user, marketer, marketer_update_request):
    client.set_user(channel_user)
    response = client.put(f"{API_URL}{marketer.id}", json=marketer_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_marketer_allowed(channel_user, marketer, marketer_update_request):
    client.set_user(channel_user)
    assign_perm(MarketerPermissions.EDIT, channel_user, marketer)
    response = client.put(f"{API_URL}{marketer.id}", json=marketer_update_request)
    assert response.status_code == 200
    marketer.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == marketer.id


@pytest.mark.django_db
def test_partial_update_marketer_not_allowed(
    channel_user, marketer, marketer_update_request
):
    client.set_user(channel_user)
    response = client.patch(f"{API_URL}{marketer.id}", json=marketer_update_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_marketer_allowed(
    channel_user, marketer, marketer_update_request
):
    client.set_user(channel_user)
    assign_perm(MarketerPermissions.EDIT, channel_user, marketer)
    response = client.patch(f"{API_URL}{marketer.id}", json=marketer_update_request)
    assert response.status_code == 200
    marketer.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == marketer.id
