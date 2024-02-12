from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from commissions.api.schemas.requests import CommissionRequest, CommissionUpdateRequest
from commissions.models import Commission
from commissions.permissions import CommissionPermissions
from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model

User = get_user_model()


def commission_list(filters: FilterSchema, actor: User):
    # if actor.is_superuser:
    commissions = Commission.objects.all()
    # else:
    #     commissions = get_objects_for_user(actor, CommissionPermissions.READ)
    commissions = filters.filter(commissions)
    return commissions


def commission_create(data: CommissionRequest, actor: User):
    if not actor.has_perm(CommissionPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        commission = Commission.objects.create(**data.dict())
    return commission


def commission_update(
    commission: Commission, data: CommissionUpdateRequest, actor: User
) -> Commission:
    if (
        not actor.has_perm(CommissionPermissions.EDIT, commission)
        and not actor.is_superuser
    ):
        raise AuthenticationError
    return model_update(commission, data, actor)


def commission_detail(commission: Commission, actor: User) -> Commission:
    return detail_model(actor, CommissionPermissions.READ, commission)


def delete_commissions(data: DeleteRequest, actor: User):
    delete_models(actor, CommissionPermissions.DELETE, data)
