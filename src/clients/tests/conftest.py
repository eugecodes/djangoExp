import pytest

from clients.api.schemas.requests import ClientRequest, ClientUpdateRequest
from clients.choices import ClientTypes, InvoiceNotificationTypes


@pytest.fixture
def client_create_request(channel):
    data = ClientRequest(
        alias="TestClient",
        channel_id=channel.id,
        fiscal_name="Fiscal Name",
        cif="12345678Z",
        client_type=ClientTypes.COMPANY,
        invoice_notification_type=InvoiceNotificationTypes.EMAIL,
        invoice_email="test@test.es",
        is_renewable=True,
    )
    yield data


@pytest.fixture
def client_update_request():
    data = ClientUpdateRequest(
        alias="NewTestClient",
        fiscal_name="New Fiscal Name",
        cif="12345678Z",
        client_type=ClientTypes.COMPANY,
        invoice_notification_type=InvoiceNotificationTypes.EMAIL,
        invoice_email="test@test.es",
        is_renewable=True,
    )
    yield data
