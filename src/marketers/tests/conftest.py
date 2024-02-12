import pytest

from marketers.api.schemas.requests import MarketerRequest


@pytest.fixture
def marketer_create_request(channel, address):
    data = MarketerRequest(
        name="TestMarketer",
        email="email@email.com",
        fiscal_name="Fiscal Name",
        cif="12345678Z",
        address_id=address.id,
    )
    yield data


@pytest.fixture
def marketer_update_request(address):
    data = MarketerRequest(
        name="NewTestMarketer",
        email="email@email.com",
        fiscal_name="Fiscal Name",
        cif="12345678Z",
        address_id=address.id,
    )
    yield data
