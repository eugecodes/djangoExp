import pytest

from contacts.api.schemas.requests import ContactRequest, ContactUpdateRequest


@pytest.fixture
def contact_create_request(channel_client):
    data = ContactRequest(
        name="TestContact",
        email="test@test.com",
        phone="+34666666666",
        is_main_contact=True,
        client_id=channel_client.id,
    )
    yield data


@pytest.fixture
def contact_update_request():
    data = ContactUpdateRequest(
        name="NewTestContact",
        email="test@test.com",
        phone="+34666666666",
        is_main_contact=True,
    )
    yield data
