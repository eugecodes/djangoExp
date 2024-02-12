from typing import Any

from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from guardian.shortcuts import get_objects_for_user
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest

User = get_user_model()


def model_update(model: Any, data: Any, actor: User) -> Any:
    with set_actor(actor):
        for attr, value in data.dict().items():
            setattr(model, attr, value)
        model.save()
    return model


def delete_models(actor: User, permission: str, data: DeleteRequest):
    queryset = get_objects_for_user(actor, permission)
    queryset.filter(id__in=data.ids).delete()


def detail_model(actor: User, permission: str, obj: Any):
    if actor.has_perm(permission, obj):
        return obj
    raise AuthenticationError
