import pytest

from addresses.services import (
    address_create,
    address_update,
)


@pytest.mark.django_db
def test_create_address_admin_user(admin_user, address_create_request):
    new_address = address_create(address_create_request, admin_user)
    assert new_address.address == address_create_request.address


@pytest.mark.django_db
def test_update_address_admin_user(admin_user, address, address_update_request):
    updatable_address = address_update(address, address_update_request, admin_user)
    assert updatable_address.address == address_update_request.address
