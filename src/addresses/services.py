from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja.errors import AuthenticationError
from ninja import FilterSchema
from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from guardian.shortcuts import get_objects_for_user
from addresses.api.schemas.requests import AddressRequest, AddressUpdateRequest
from addresses.permissions import AddressPermissions
from addresses.models import Address


User = get_user_model()

def address_list(filters: FilterSchema, actor: User):
    if actor.is_superuser:
        addresses = Address.objects.all()
    else:
        addresses = get_objects_for_user(actor, AddressPermissions.READ)
    addresses = filters.filter(addresses)
    return addresses


def address_create(data: AddressRequest, actor: User):
    if not actor.has_perm(AddressPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        address = Address.objects.create(**data.dict())
    return address


def address_update(address: Address, data: AddressUpdateRequest, actor: User) -> Address:
    if not actor.has_perm(AddressPermissions.EDIT, address) and not actor.is_superuser:
        raise AuthenticationError
    return model_update(address, data, actor)


def address_detail(address: Address, actor: User) -> Address:
    return detail_model(actor, AddressPermissions.READ, address)


def delete_addresses(data: DeleteRequest, actor: User):
    delete_models(actor, AddressPermissions.DELETE, data)
