import pytest
from ninja.errors import AuthenticationError
from guardian.shortcuts import assign_perm
from {{ cookiecutter.app_slug_plural }}.permissions import {{ cookiecutter.app_name }}Permissions
from {{ cookiecutter.app_slug_plural }}.services import (
    {{ cookiecutter.app_slug }}_create,
    {{ cookiecutter.app_slug }}_update,
)


@pytest.mark.django_db
def test_create_{{ cookiecutter.app_slug }}_channel_user_not_allowed(channel_user, {{ cookiecutter.app_slug }}_create_request):
    with pytest.raises(AuthenticationError):
        {{ cookiecutter.app_slug }}_create({{ cookiecutter.app_slug }}_create_request, channel_user)

@pytest.mark.django_db
def test_create_{{ cookiecutter.app_slug }}_channel_user_allowed(channel_user, {{ cookiecutter.app_slug }}_create_request):
    assign_perm({{ cookiecutter.app_name }}Permissions.CREATE, channel_user)
    new_{{ cookiecutter.app_slug }} = {{ cookiecutter.app_slug }}_create({{ cookiecutter.app_slug }}_create_request, channel_user)
    assert new_{{ cookiecutter.app_slug }}.name == {{ cookiecutter.app_slug }}_create_request.name


@pytest.mark.django_db
def test_update_{{ cookiecutter.app_slug }}_channel_user_not_allowed(channel_user, {{ cookiecutter.app_slug }}, {{ cookiecutter.app_slug }}_update_request):
    with pytest.raises(AuthenticationError):
        {{ cookiecutter.app_slug }}_update({{ cookiecutter.app_slug }}, {{ cookiecutter.app_slug }}_update_request, channel_user)


@pytest.mark.django_db
def test_update_{{ cookiecutter.app_slug }}_channel_user_allowed(channel_user, {{ cookiecutter.app_slug }}, {{ cookiecutter.app_slug }}_update_request):
    assign_perm({{ cookiecutter.app_name }}Permissions.EDIT, channel_user, {{ cookiecutter.app_slug }})
    updatable_{{ cookiecutter.app_slug }} = {{ cookiecutter.app_slug }}_update({{ cookiecutter.app_slug }}, {{ cookiecutter.app_slug }}_update_request, channel_user)
    assert updatable_{{ cookiecutter.app_slug }}.name == {{ cookiecutter.app_slug }}_update_request.name