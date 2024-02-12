import pytest

from contracts.services import (
    contract_create,
    contract_update,
)


@pytest.mark.django_db
def test_create_contract_admin_user(admin_user, contract_create_request):
    new_contract = contract_create(contract_create_request, admin_user)
    assert (
        new_contract.signature_first_name
        == contract_create_request.signature_first_name
    )


@pytest.mark.django_db
def test_update_contract_admin_user(admin_user, contract, contract_update_request):
    updatable_contract = contract_update(contract, contract_update_request, admin_user)
    assert (
        updatable_contract.signature_first_name
        == contract_update_request.signature_first_name
    )
