from auditlog.context import set_actor
from django.conf import settings
from django.contrib.auth import get_user_model
from ninja import FilterSchema
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from users.api.schemas.requests import (
    UserRequest,
)
from users.permissions import UserPermissions

User = get_user_model()


def user_list(filters: FilterSchema, actor: User):
    if not actor.has_perm(UserPermissions.READ) and not actor.is_superuser:
        raise AuthenticationError
    users = User.objects.exclude(email=settings.ANONYMOUS_EMAIL).exclude(id=actor.id)
    users = filters.filter(users)
    return users


def user_create(data: UserRequest, actor: User):
    with set_actor(actor):
        user = User.objects.create_user(**data.dict())
    return user


def user_update(user: User, data: UserRequest, actor: User) -> User:
    return model_update(user, data, actor)


def user_detail(user: User, actor: User) -> User:
    return detail_model(actor, UserPermissions.READ, user)


def delete_users(data: DeleteRequest):
    delete_models(User, UserPermissions.DELETE, data)
