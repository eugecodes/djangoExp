from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from channels.api.schemas.requests import ChannelRequest
from channels.models import Channel
from channels.permissions import ChannelPermissions
from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model

User = get_user_model()


def channel_list(filters: FilterSchema, actor: User):
    if not actor.has_perm(ChannelPermissions.READ) and not actor.is_superuser:
        raise AuthenticationError
    channels = Channel.objects.all()
    channels = filters.filter(channels)
    return channels


def channel_create(data: ChannelRequest, actor: User) -> Channel:
    # actor.has_perm(ChannelPermissions.EDIT, task)
    with set_actor(actor):
        channel = Channel.objects.create(**data.dict())
    return channel


def channel_update(channel: Channel, data: ChannelRequest, actor: User) -> Channel:
    return model_update(channel, data, actor)


def channel_detail(channel: Channel, actor: User) -> Channel:
    return detail_model(actor, ChannelPermissions.READ, channel)


def delete_channels(data: DeleteRequest, actor: User):
    delete_models(actor, ChannelPermissions.DELETE, data)
