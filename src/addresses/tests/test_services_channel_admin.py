import pytest

from addresses.services import (
    address_create,
    address_update,
)


@pytest.mark.django_db
def test_create_address_channel_admin(channel_admin, address_create_request):
    new_address = address_create(address_create_request, channel_admin)
    assert new_address.address == address_create_request.address


@pytest.mark.django_db
def test_update_address_channel_admin(channel_admin, address, address_update_request):
    updatable_address = address_update(address, address_update_request, channel_admin)
    assert updatable_address.address == address_update_request.address
