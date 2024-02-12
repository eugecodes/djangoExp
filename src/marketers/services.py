from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from marketers.api.schemas.requests import MarketerRequest
from marketers.models import Marketer
from marketers.permissions import MarketerPermissions

User = get_user_model()


def marketer_list(filters: FilterSchema, actor: User):
    marketers = Marketer.objects.all()
    marketers = filters.filter(marketers)
    return marketers


def marketer_create(data: MarketerRequest, actor: User):
    if not actor.has_perm(MarketerPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        marketer = Marketer.objects.create(**data.dict())
    return marketer


def marketer_update(marketer: Marketer, data: MarketerRequest, actor: User) -> Marketer:
    if (
        not actor.has_perm(MarketerPermissions.EDIT, marketer)
        and not actor.is_superuser
    ):
        raise AuthenticationError
    return model_update(marketer, data, actor)


def marketer_detail(marketer: Marketer, actor: User) -> Marketer:
    return detail_model(actor, MarketerPermissions.READ, marketer)


def delete_marketers(data: DeleteRequest, actor: User):
    delete_models(actor, MarketerPermissions.DELETE, data)
