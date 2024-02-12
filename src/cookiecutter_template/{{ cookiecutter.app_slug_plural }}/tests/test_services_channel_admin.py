import pytest

from {{ cookiecutter.app_slug_plural }}.services import (
    {{ cookiecutter.app_slug }}_create,
    {{ cookiecutter.app_slug }}_update,
)


@pytest.mark.django_db
def test_create_{{ cookiecutter.app_slug }}_channel_admin(channel_admin, {{ cookiecutter.app_slug }}_create_request):
    new_{{ cookiecutter.app_slug }} = {{ cookiecutter.app_slug }}_create({{ cookiecutter.app_slug }}_create_request, channel_admin)
    assert new_{{ cookiecutter.app_slug }}.name == {{ cookiecutter.app_slug }}_create_request.name


@pytest.mark.django_db
def test_update_{{ cookiecutter.app_slug }}_channel_admin(channel_admin, {{ cookiecutter.app_slug }}, {{ cookiecutter.app_slug }}_update_request):
    updatable_{{ cookiecutter.app_slug }} = {{ cookiecutter.app_slug }}_update({{ cookiecutter.app_slug }}, {{ cookiecutter.app_slug }}_update_request, channel_admin)
    assert updatable_{{ cookiecutter.app_slug }}.name == {{ cookiecutter.app_slug }}_update_request.name
