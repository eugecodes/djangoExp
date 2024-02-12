from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja.errors import AuthenticationError
from ninja import FilterSchema
from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from guardian.shortcuts import get_objects_for_user
from suggested_rates.api.schemas.requests import SuggestedRateRequest, SuggestedRateUpdateRequest
from suggested_rates.permissions import SuggestedRatePermissions
from suggested_rates.models import SuggestedRate


User = get_user_model()

def suggested_rate_list(filters: FilterSchema, actor: User):
    if actor.is_superuser:
        suggested_rates = SuggestedRate.objects.all()
    else:
        suggested_rates = get_objects_for_user(actor, SuggestedRatePermissions.READ)
    suggested_rates = filters.filter(suggested_rates)
    return suggested_rates


def suggested_rate_create(data: SuggestedRateRequest, actor: User):
    if not actor.has_perm(SuggestedRatePermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        suggested_rate = SuggestedRate.objects.create(**data.dict())
    return suggested_rate


def suggested_rate_update(suggested_rate: SuggestedRate, data: SuggestedRateUpdateRequest, actor: User) -> SuggestedRate:
    if not actor.has_perm(SuggestedRatePermissions.EDIT, suggested_rate) and not actor.is_superuser:
        raise AuthenticationError
    return model_update(suggested_rate, data, actor)


def suggested_rate_detail(suggested_rate: SuggestedRate, actor: User) -> SuggestedRate:
    return detail_model(actor, SuggestedRatePermissions.READ, suggested_rate)


def delete_suggested_rates(data: DeleteRequest, actor: User):
    delete_models(actor, SuggestedRatePermissions.DELETE, data)
