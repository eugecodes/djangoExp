import pytest
from django.contrib.auth import get_user_model

from conftest import PASSWORD
from users.api.schemas.requests import UserLoginRequest, UserRequest
from users.models import Token
from users.services.login import (
    get_user_by_token,
    get_or_create_token,
    get_or_create_user_token,
    login_user,
    logout_user,
)
from users.services.user import user_update, user_create

User = get_user_model()


@pytest.mark.django_db
def test_get_user_by_token(admin_user):
    token = get_or_create_token(admin_user)
    res_user = get_user_by_token(token.token)

    assert res_user == admin_user


@pytest.mark.django_db
def test_get_or_create_token(admin_user):
    token = get_or_create_token(admin_user)

    assert Token.objects.first() == token


@pytest.mark.django_db
def test_get_or_create_user_token(admin_user):
    token = get_or_create_user_token(admin_user)

    assert Token.objects.first() == token


@pytest.mark.django_db
def test_login_user(admin_user):
    login_data = UserLoginRequest(email=admin_user.email, password=PASSWORD)
    token = login_user(login_data)

    assert Token.objects.first() == token


@pytest.mark.django_db
def test_logout_user(admin_user):
    login_data = UserLoginRequest(email=admin_user.email, password=PASSWORD)
    token = login_user(login_data)
    assert Token.objects.first() == token
    logout_user(admin_user)
    assert Token.objects.count() == 0


@pytest.mark.django_db
def test_create_user(admin_user):
    data = UserRequest(
        first_name="first_name", last_name="last_name", email="email@email.com"
    )
    new_user = user_create(data, admin_user)
    assert new_user.first_name == "first_name"
    assert new_user.last_name == "last_name"
    assert new_user.email == "email@email.com"


@pytest.mark.django_db
def test_update_user(admin_user):
    data = UserRequest(
        first_name="first_name", last_name="last_name", email="email@email.com"
    )
    updatable_user = User.objects.create(email=f"testuser@test.es")
    updatable_user = user_update(updatable_user, data, admin_user)
    assert updatable_user.first_name == "first_name"
    assert updatable_user.last_name == "last_name"
    assert updatable_user.email == "email@email.com"
