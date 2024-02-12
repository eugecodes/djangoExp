from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from rates.api.schemas.requests import RateRequest
from rates.models import Rate
from rates.permissions import RatePermissions

User = get_user_model()


def rate_list(filters: FilterSchema, actor: User):
    rates = Rate.objects.all()
    rates = filters.filter(rates)
    return rates


def rate_create(data: RateRequest, actor: User):
    if not actor.has_perm(RatePermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        rate = Rate.objects.create(**data.dict())
    return rate


def rate_update(rate: Rate, data: RateRequest, actor: User) -> Rate:
    if not actor.has_perm(RatePermissions.EDIT, rate) and not actor.is_superuser:
        raise AuthenticationError
    return model_update(rate, data, actor)


def rate_detail(rate: Rate, actor: User) -> Rate:
    return detail_model(actor, RatePermissions.READ, rate)


def delete_rates(data: DeleteRequest, actor: User):
    delete_models(actor, RatePermissions.DELETE, data)
