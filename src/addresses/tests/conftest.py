import pytest

from addresses.api.schemas.requests import AddressRequest, AddressUpdateRequest


@pytest.fixture
def address_create_request(channel):
    data = AddressRequest(
        channel_id=channel.id,
        address="TestAddress",
        postal_code="22222",
        city="Madrid",
        province="Madrid",
    )
    yield data


@pytest.fixture
def address_update_request():
    data = AddressUpdateRequest(
        address="TestAddress", postal_code="22222", city="Madrid", province="Madrid"
    )
    yield data
