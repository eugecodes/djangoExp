import pytest

from common.client import client
from marketers.models import Marketer

API_URL = f"/marketers/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, marketer):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == Marketer.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_marketer_admin_user(admin_user, marketer_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json=marketer_create_request)
    new_marketer = Marketer.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_marketer.id


@pytest.mark.django_db
def test_update_marketer_admin_user(admin_user, marketer, marketer_update_request):
    client.set_user(admin_user)
    response = client.put(f"{API_URL}{marketer.id}", json=marketer_update_request)
    marketer.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == marketer.id
    assert json_response["name"] == marketer_update_request.name


@pytest.mark.django_db
def test_partial_update_marketer_admin_user(
    admin_user, marketer, marketer_update_request
):
    client.set_user(admin_user)
    response = client.patch(f"{API_URL}{marketer.id}", json=marketer_update_request)
    marketer.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == marketer.id
    assert json_response["name"] == marketer_update_request.name
