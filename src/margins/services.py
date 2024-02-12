from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from margins.api.schemas.requests import MarginRequest
from margins.models import Margin
from margins.permissions import MarginPermissions

User = get_user_model()


def margin_list(filters: FilterSchema, actor: User):
    # if actor.is_superuser:
    margins = Margin.objects.all()
    # else:
    #     margins = get_objects_for_user(actor, MarginPermissions.READ)
    margins = filters.filter(margins)
    return margins


def margin_create(data: MarginRequest, actor: User):
    if not actor.has_perm(MarginPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        margin = Margin.objects.create(**data.dict())
    return margin


def margin_update(margin: Margin, data: MarginRequest, actor: User) -> Margin:
    if not actor.has_perm(MarginPermissions.EDIT, margin) and not actor.is_superuser:
        raise AuthenticationError
    return model_update(margin, data, actor)


def margin_detail(margin: Margin, actor: User) -> Margin:
    return detail_model(actor, MarginPermissions.READ, margin)


def delete_margins(data: DeleteRequest, actor: User):
    delete_models(actor, MarginPermissions.DELETE, data)
