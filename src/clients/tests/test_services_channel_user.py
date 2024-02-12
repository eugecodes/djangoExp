import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from clients.permissions import ClientPermissions
from clients.services import (
    client_create,
    client_update,
)


@pytest.mark.django_db
def test_create_client_channel_user_not_allowed(channel_user, client_create_request):
    with pytest.raises(AuthenticationError):
        client_create(client_create_request, channel_user)


@pytest.mark.django_db
def test_create_client_channel_user_allowed(channel_user, client_create_request):
    assign_perm(ClientPermissions.CREATE, channel_user)
    new_client = client_create(client_create_request, channel_user)
    assert new_client.alias == client_create_request.alias
    assert new_client.fiscal_name == client_create_request.fiscal_name
    assert new_client.cif == client_create_request.cif


@pytest.mark.django_db
def test_update_client_channel_user_not_allowed(
    channel_user, channel_client, client_update_request
):
    with pytest.raises(AuthenticationError):
        client_update(channel_client, client_update_request, channel_user)


@pytest.mark.django_db
def test_update_client_channel_user_allowed(
    channel_user, channel_client, client_update_request
):
    assign_perm(ClientPermissions.EDIT, channel_user, channel_client)
    updatable_client = client_update(
        channel_client, client_update_request, channel_user
    )
    assert updatable_client.alias == client_update_request.alias
    assert updatable_client.fiscal_name == client_update_request.fiscal_name
    assert updatable_client.cif == client_update_request.cif
