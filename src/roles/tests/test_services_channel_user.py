import pytest
from ninja.errors import AuthenticationError

from roles.services import (
    role_create,
    role_update,
)


@pytest.mark.django_db
def test_create_role_channel_user(channel_user, role_create_request):
    with pytest.raises(AuthenticationError):
        role_create(role_create_request, channel_user)


@pytest.mark.django_db
def test_update_role_channel_user(
    channel_user, admin_channel_role, role_update_request
):
    role, group = admin_channel_role
    with pytest.raises(AuthenticationError):
        role_update(role, role_update_request, channel_user)
