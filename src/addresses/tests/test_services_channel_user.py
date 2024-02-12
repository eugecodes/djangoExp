import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from addresses.permissions import AddressPermissions
from addresses.services import (
    address_create,
    address_update,
)


@pytest.mark.django_db
def test_create_address_channel_user_not_allowed(channel_user, address_create_request):
    with pytest.raises(AuthenticationError):
        address_create(address_create_request, channel_user)


@pytest.mark.django_db
def test_create_address_channel_user_allowed(channel_user, address_create_request):
    assign_perm(AddressPermissions.CREATE, channel_user)
    new_address = address_create(address_create_request, channel_user)
    assert new_address.address == address_create_request.address


@pytest.mark.django_db
def test_update_address_channel_user_not_allowed(
    channel_user, address, address_update_request
):
    with pytest.raises(AuthenticationError):
        address_update(address, address_update_request, channel_user)


@pytest.mark.django_db
def test_update_address_channel_user_allowed(
    channel_user, address, address_update_request
):
    assign_perm(AddressPermissions.EDIT, channel_user, address)
    updatable_address = address_update(address, address_update_request, channel_user)
    assert updatable_address.address == address_update_request.address
