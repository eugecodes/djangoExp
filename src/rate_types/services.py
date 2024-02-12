from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from rate_types.api.schemas.requests import RateTypeRequest
from rate_types.models import RateType
from rate_types.permissions import RateTypePermissions

User = get_user_model()


def rate_types_list(filters: FilterSchema, actor: User):
    rate_types = RateType.objects.all()
    rate_types = filters.filter(rate_types)
    return rate_types


def rate_type_create(data: RateTypeRequest, actor: User) -> RateType:
    if not actor.has_perm(RateTypePermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        rate_type = RateType.objects.create(**data.dict())
    return rate_type


def rate_type_update(
    rate_type: RateType, data: RateTypeRequest, actor: User
) -> RateType:
    if (
        not actor.has_perm(RateTypePermissions.EDIT, rate_type)
        and not actor.is_superuser
    ):
        raise AuthenticationError
    return model_update(rate_type, data, actor)


def rate_type_detail(rate_type: RateType, actor: User) -> RateType:
    return detail_model(actor, RateTypePermissions.READ, rate_type)


def delete_rate_types(data: DeleteRequest, actor: User):
    delete_models(actor, RateTypePermissions.DELETE, data)
