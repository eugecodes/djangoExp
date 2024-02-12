import pytest

from contracts.api.schemas.requests import ContractRequest, ContractUpdateRequest


@pytest.fixture
def contract_create_request(channel, channel_client, rate, saving_study, supply_point):
    data = ContractRequest(
        channel_id=channel.id,
        client_id=channel_client.id,
        supply_point_id=supply_point.id,
        rate_id=rate.id,
        signature_first_name="signature_first_name",
        signature_last_name="signature_last_name",
    )
    yield data


@pytest.fixture
def contract_update_request():
    data = ContractUpdateRequest(
        signature_first_name="signature_first_name",
        signature_last_name="signature_last_name",
    )
    yield data
