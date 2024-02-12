from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from energy_costs.api.schemas.requests import EnergyCostRequest, EnergyCostUpdateRequest
from energy_costs.models import EnergyCost
from energy_costs.permissions import EnergyCostPermissions

User = get_user_model()


def energy_cost_list(filters: FilterSchema, actor: User):
    energy_costs = EnergyCost.objects.all()
    energy_costs = filters.filter(energy_costs)
    return energy_costs


def energy_cost_create(data: EnergyCostRequest, actor: User):
    if not actor.has_perm(EnergyCostPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        energy_cost = EnergyCost.objects.create(**data.dict())
    return energy_cost


def energy_cost_update(
    energy_cost: EnergyCost, data: EnergyCostUpdateRequest, actor: User
) -> EnergyCost:
    if (
        not actor.has_perm(EnergyCostPermissions.EDIT, energy_cost)
        and not actor.is_superuser
    ):
        raise AuthenticationError
    return model_update(energy_cost, data, actor)


def energy_cost_detail(energy_cost: EnergyCost, actor: User) -> EnergyCost:
    return detail_model(actor, EnergyCostPermissions.READ, energy_cost)


def delete_energy_costs(data: DeleteRequest, actor: User):
    delete_models(actor, EnergyCostPermissions.DELETE, data)
