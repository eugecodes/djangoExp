import pytest
from django.contrib.auth import get_user_model

from common.client import client
from common.pagination import EMPTY_LIST_RESPONSE
from conftest import PASSWORD
from users.api.schemas.requests import UserRequest

User = get_user_model()


@pytest.mark.django_db
def test_login(admin_user):
    data = {"email": admin_user.email, "password": PASSWORD}
    response = client.post("/users/login", json=data)
    assert response.status_code == 200
    assert response.json()["user"]["email"] == admin_user.email
    assert response.json()["user"]["id"] == admin_user.id


@pytest.mark.django_db
def test_login_invalid(admin_user):
    data = {"email": admin_user.email, "password": "password"}
    response = client.post("/users/login", json=data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_list_empty(admin_user):
    client.set_user(admin_user)
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == EMPTY_LIST_RESPONSE


@pytest.mark.django_db
def test_get_list(admin_user):
    user1 = User.objects.create(email=f"testuser@test.es")
    client.set_user(admin_user)
    response = client.get("/users/")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["items"][0]["id"] == user1.id
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_user(admin_user):
    client.set_user(admin_user)
    data = UserRequest(
        first_name="first_name", last_name="last_name", email="email@email.com"
    )
    response = client.post("/users/", json=data)
    new_user = User.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_user.id
    assert json_response["first_name"] == new_user.first_name == "first_name"
    assert json_response["last_name"] == new_user.last_name == "last_name"


@pytest.mark.django_db
def test_update_user(admin_user):
    client.set_user(admin_user)
    data = UserRequest(
        first_name="first_name", last_name="last_name", email="email@email.com"
    )
    new_user = User.objects.create(email=f"testuser@test.es")
    response = client.put(f"/users/{new_user.id}", json=data)
    new_user.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == new_user.id
    assert json_response["first_name"] == new_user.first_name == "first_name"
    assert json_response["last_name"] == new_user.last_name == "last_name"


@pytest.mark.django_db
def test_partial_update_user(admin_user):
    client.set_user(admin_user)
    data = UserRequest(
        first_name="first_name", last_name="last_name", email="email@email.com"
    )
    new_user = User.objects.create(email=f"testuser@test.es")
    response = client.patch(f"/users/{new_user.id}", json=data)
    new_user.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == new_user.id
    assert json_response["first_name"] == new_user.first_name == "first_name"
    assert json_response["last_name"] == new_user.last_name == "last_name"
