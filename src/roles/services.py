from auditlog.context import set_actor
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from guardian.shortcuts import assign_perm, get_objects_for_user
from ninja.errors import AuthenticationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from roles.api.schemas.requests import (
    RoleRequest,
)
from roles.models import Role
from roles.permissions import RolePermissions

User = get_user_model()


def add_role_permissions(role: Role):
    if role.channel:
        admin_role = role.channel.roles.filter(admin_role=True).first()
        assign_perm(RolePermissions.DELETE, admin_role.group, role)
        assign_perm(RolePermissions.EDIT, admin_role.group, role)
        assign_perm(RolePermissions.READ, admin_role.group, role)
    channel_support_role = Role.objects.get(name=settings.DEFAULT_CHANNEL_SUPPORT)
    assign_perm(RolePermissions.DELETE, channel_support_role.group, role)
    assign_perm(RolePermissions.EDIT, channel_support_role.group, role)
    assign_perm(RolePermissions.READ, channel_support_role.group, role)


def role_create(data: RoleRequest, actor: User):
    if not actor.has_perm(RolePermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        create_data = data.dict()
        group_name = f"{data.name}"
        if actor.channel is not None:
            create_data["channel"] = actor.channel
            group_name = f"{data.name} - {actor.channel.name}"
        group = Group.objects.create(
            name=group_name,
        )
        create_data["group"] = group
        role = Role.objects.create(**create_data)
        add_role_permissions(role)
    return role


def role_update(role: Role, data: RoleRequest, actor: User) -> Role:
    if not actor.has_perm(RolePermissions.EDIT, role) and not actor.is_superuser:
        raise AuthenticationError
    return model_update(role, data, actor)


def delete_roles(data: DeleteRequest, actor: User):
    delete_models(actor, RolePermissions.DELETE, data)


def role_detail(role: Role, actor: User) -> Role:
    return detail_model(actor, RolePermissions.READ, role)


def roles_list(actor: User):
    if actor.has_perm(RolePermissions.READ) or actor.is_superuser:
        return Role.objects.all()
    return get_objects_for_user(actor, RolePermissions.READ)
