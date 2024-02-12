from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from costs.api.schemas.requests import OtherCostRequest, OtherCostUpdateRequest
from costs.models import OtherCost
from costs.permissions import OtherCostPermissions

User = get_user_model()


def cost_list(filters: FilterSchema, actor: User):
    costs = OtherCost.objects.all()
    costs = filters.filter(costs)
    return costs


def cost_create(data: OtherCostRequest, actor: User):
    if not actor.has_perm(OtherCostPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        cost = OtherCost.objects.create(**data.dict())
    return cost


def cost_update(
    cost: OtherCost, data: OtherCostUpdateRequest, actor: User
) -> OtherCost:
    if not actor.has_perm(OtherCostPermissions.EDIT, cost) and not actor.is_superuser:
        raise AuthenticationError
    return model_update(cost, data, actor)


def cost_detail(cost: OtherCost, actor: User) -> OtherCost:
    return detail_model(actor, OtherCostPermissions.READ, cost)


def delete_costs(data: DeleteRequest, actor: User):
    delete_models(actor, OtherCostPermissions.DELETE, data)
