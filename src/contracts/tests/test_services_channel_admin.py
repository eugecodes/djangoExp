import pytest

from contracts.services import (
    contract_create,
    contract_update,
)


@pytest.mark.django_db
def test_create_contract_channel_admin(channel_admin, contract_create_request):
    new_contract = contract_create(contract_create_request, channel_admin)
    assert (
        new_contract.signature_first_name
        == contract_create_request.signature_first_name
    )


@pytest.mark.django_db
def test_update_contract_channel_admin(
    channel_admin, contract, contract_update_request
):
    updatable_contract = contract_update(
        contract, contract_update_request, channel_admin
    )
    assert (
        updatable_contract.signature_first_name
        == contract_update_request.signature_first_name
    )
