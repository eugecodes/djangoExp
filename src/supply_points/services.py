from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from djmoney.money import Money
from guardian.shortcuts import get_objects_for_user
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from supply_points.api.schemas.requests import (
    SupplyPointRequest,
    SupplyPointUpdateRequest,
)
from supply_points.models import SupplyPoint
from supply_points.permissions import SupplyPointPermissions

User = get_user_model()


def supply_point_list(filters: FilterSchema, actor: User):
    if actor.is_superuser:
        supply_points = SupplyPoint.objects.all()
    else:
        supply_points = get_objects_for_user(actor, SupplyPointPermissions.READ)
    supply_points = filters.filter(supply_points)
    return supply_points


def supply_point_create(data: SupplyPointRequest, actor: User):
    if not actor.has_perm(SupplyPointPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        data.counter_price = Money(
            data.counter_price_amount,
            currency=data.counter_price_currency,
        )
        del (data.counter_price_amount, data.counter_price_currency)
        supply_point = SupplyPoint.objects.create(**data.dict())
    return supply_point


def supply_point_update(
    supply_point: SupplyPoint, data: SupplyPointUpdateRequest, actor: User
) -> SupplyPoint:
    if (
        not actor.has_perm(SupplyPointPermissions.EDIT, supply_point)
        and not actor.is_superuser
    ):
        raise AuthenticationError

    data.counter_price = Money(
        data.counter_price_amount,
        currency=data.counter_price_currency,
    )
    return model_update(supply_point, data, actor)


def supply_point_detail(supply_point: SupplyPoint, actor: User) -> SupplyPoint:
    return detail_model(actor, SupplyPointPermissions.READ, supply_point)


def delete_supply_points(data: DeleteRequest, actor: User):
    delete_models(actor, SupplyPointPermissions.DELETE, data)
