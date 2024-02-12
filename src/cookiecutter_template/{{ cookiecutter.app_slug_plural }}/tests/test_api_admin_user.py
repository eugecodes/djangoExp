import pytest

from common.client import client
from {{ cookiecutter.app_slug_plural }}.models import {{ cookiecutter.app_name }}

API_URL = f"/{{ cookiecutter.app_slug_plural }}/"


@pytest.mark.django_db
def test_get_list_admin_user(admin_user, {{ cookiecutter.app_slug }}):
    client.set_user(admin_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == {{ cookiecutter.app_name }}.objects.count()
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_{{ cookiecutter.app_slug }}_admin_user(admin_user, {{ cookiecutter.app_slug }}_create_request):
    client.set_user(admin_user)
    response = client.post(API_URL, json={{ cookiecutter.app_slug }}_create_request)
    new_{{ cookiecutter.app_slug }} = {{ cookiecutter.app_name }}.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_{{ cookiecutter.app_slug }}.id
    assert json_response["name"] == {{ cookiecutter.app_slug }}_create_request.name


@pytest.mark.django_db
def test_update_{{ cookiecutter.app_slug }}_admin_user(admin_user, {{ cookiecutter.app_slug }}, {{ cookiecutter.app_slug }}_update_request):
    client.set_user(admin_user)
    response = client.put(f"{API_URL}{{'{'}}{{ cookiecutter.app_slug }}.id}", json={{ cookiecutter.app_slug }}_update_request)
    {{ cookiecutter.app_slug }}.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == {{ cookiecutter.app_slug }}.id
    assert json_response["name"] == {{ cookiecutter.app_slug }}_update_request.name


@pytest.mark.django_db
def test_partial_update_{{ cookiecutter.app_slug }}_admin_user(admin_user, {{ cookiecutter.app_slug }}, {{ cookiecutter.app_slug }}_update_request):
    client.set_user(admin_user)
    response = client.patch(f"{API_URL}{{'{'}}{{ cookiecutter.app_slug }}.id}", json={{ cookiecutter.app_slug }}_update_request)
    {{ cookiecutter.app_slug }}.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == {{ cookiecutter.app_slug }}.id
    assert json_response["name"] == {{ cookiecutter.app_slug }}_update_request.name
