from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from guardian.shortcuts import get_objects_for_user
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from clients.api.schemas.requests import (
    ClientRequest,
)
from clients.models import Client
from clients.permissions import ClientPermissions
from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model

User = get_user_model()


def client_list(filters: FilterSchema, actor: User):
    if actor.is_superuser:
        clients = Client.objects.all()
    else:
        clients = get_objects_for_user(actor, ClientPermissions.READ)
    clients = filters.filter(clients)
    return clients


def client_create(data: ClientRequest, actor: User) -> Client:
    if not actor.has_perm(ClientPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        client_data = data.dict()
        if actor.channel:
            client_data["channel_id"] = actor.channel_id
        client = Client.objects.create(**client_data)
    return client


def client_update(client: Client, data: ClientRequest, actor: User) -> Client:
    if not actor.has_perm(ClientPermissions.EDIT, client) and not actor.is_superuser:
        raise AuthenticationError
    return model_update(client, data, actor)


def client_detail(client: Client, actor: User) -> Client:
    return detail_model(actor, ClientPermissions.READ, client)


def delete_clients(data: DeleteRequest, actor: User):
    delete_models(actor, ClientPermissions.DELETE, data)
