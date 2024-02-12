from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja.errors import AuthenticationError
from ninja import FilterSchema
from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from guardian.shortcuts import get_objects_for_user
from contracts.api.schemas.requests import ContractRequest, ContractUpdateRequest
from contracts.permissions import ContractPermissions
from contracts.models import Contract


User = get_user_model()

def contract_list(filters: FilterSchema, actor: User):
    if actor.is_superuser:
        contracts = Contract.objects.all()
    else:
        contracts = get_objects_for_user(actor, ContractPermissions.READ)
    contracts = filters.filter(contracts)
    return contracts


def contract_create(data: ContractRequest, actor: User):
    if not actor.has_perm(ContractPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        contract = Contract.objects.create(**data.dict())
    return contract


def contract_update(contract: Contract, data: ContractUpdateRequest, actor: User) -> Contract:
    if not actor.has_perm(ContractPermissions.EDIT, contract) and not actor.is_superuser:
        raise AuthenticationError
    return model_update(contract, data, actor)


def contract_detail(contract: Contract, actor: User) -> Contract:
    return detail_model(actor, ContractPermissions.READ, contract)


def delete_contracts(data: DeleteRequest, actor: User):
    delete_models(actor, ContractPermissions.DELETE, data)
