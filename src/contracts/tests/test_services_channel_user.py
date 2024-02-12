import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from contracts.permissions import ContractPermissions
from contracts.services import (
    contract_create,
    contract_update,
)


@pytest.mark.django_db
def test_create_contract_channel_user_not_allowed(
    channel_user, contract_create_request
):
    with pytest.raises(AuthenticationError):
        contract_create(contract_create_request, channel_user)


@pytest.mark.django_db
def test_create_contract_channel_user_allowed(channel_user, contract_create_request):
    assign_perm(ContractPermissions.CREATE, channel_user)
    new_contract = contract_create(contract_create_request, channel_user)
    assert (
        new_contract.signature_first_name
        == contract_create_request.signature_first_name
    )


@pytest.mark.django_db
def test_update_contract_channel_user_not_allowed(
    channel_user, contract, contract_update_request
):
    with pytest.raises(AuthenticationError):
        contract_update(contract, contract_update_request, channel_user)


@pytest.mark.django_db
def test_update_contract_channel_user_allowed(
    channel_user, contract, contract_update_request
):
    assign_perm(ContractPermissions.EDIT, channel_user, contract)
    updatable_contract = contract_update(
        contract, contract_update_request, channel_user
    )
    assert (
        updatable_contract.signature_first_name
        == contract_update_request.signature_first_name
    )
