import pytest

from roles.services import (
    role_create,
    role_update,
)


@pytest.mark.django_db
def test_create_role_channel_admin(channel_admin, role_create_request):
    new_role = role_create(role_create_request, channel_admin)
    assert new_role.name == role_create_request.name


@pytest.mark.django_db
def test_update_role_channel_admin(
    channel_admin, admin_channel_role, role_update_request
):
    role, group = admin_channel_role
    updatable_role = role_update(role, role_update_request, channel_admin)
    assert updatable_role.name == role_update_request.name
