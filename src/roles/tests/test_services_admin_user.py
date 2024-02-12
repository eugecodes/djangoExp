import pytest

from roles.services import (
    role_create,
    role_update,
)


@pytest.mark.django_db
def test_create_role_admin_user(admin_user, role_create_request):
    new_role = role_create(role_create_request, admin_user)
    assert new_role.name == role_create_request.name


@pytest.mark.django_db
def test_update_role_admin_user(admin_user, role, role_update_request):
    updatable_role = role_update(role, role_update_request, admin_user)
    assert updatable_role.name == role_update_request.name
