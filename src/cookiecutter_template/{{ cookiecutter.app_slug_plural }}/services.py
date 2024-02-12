from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from ninja.errors import AuthenticationError
from ninja import FilterSchema
from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from guardian.shortcuts import get_objects_for_user
from {{ cookiecutter.app_slug_plural }}.api.schemas.requests import {{ cookiecutter.app_name }}Request, {{ cookiecutter.app_name }}UpdateRequest
from {{ cookiecutter.app_slug_plural }}.permissions import {{ cookiecutter.app_name }}Permissions
from {{ cookiecutter.app_slug_plural }}.models import {{ cookiecutter.app_name }}


User = get_user_model()

def {{ cookiecutter.app_slug }}_list(filters: FilterSchema, actor: User):
    if actor.is_superuser:
        {{ cookiecutter.app_slug_plural }} = {{ cookiecutter.app_name }}.objects.all()
    else:
        {{ cookiecutter.app_slug_plural }} = get_objects_for_user(actor, {{ cookiecutter.app_name }}Permissions.READ)
    {{ cookiecutter.app_slug_plural }} = filters.filter({{ cookiecutter.app_slug_plural }})
    return {{ cookiecutter.app_slug_plural }}


def {{ cookiecutter.app_slug }}_create(data: {{ cookiecutter.app_name }}Request, actor: User):
    if not actor.has_perm({{ cookiecutter.app_name }}Permissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    with set_actor(actor):
        {{ cookiecutter.app_slug }} = {{ cookiecutter.app_name }}.objects.create(**data.dict())
    return {{ cookiecutter.app_slug }}


def {{ cookiecutter.app_slug }}_update({{ cookiecutter.app_slug }}: {{ cookiecutter.app_name }}, data: {{ cookiecutter.app_name }}UpdateRequest, actor: User) -> {{ cookiecutter.app_name }}:
    if not actor.has_perm({{ cookiecutter.app_name }}Permissions.EDIT, {{ cookiecutter.app_slug }}) and not actor.is_superuser:
        raise AuthenticationError
    return model_update({{ cookiecutter.app_slug }}, data, actor)


def {{ cookiecutter.app_slug }}_detail({{ cookiecutter.app_slug }}: {{ cookiecutter.app_name }}, actor: User) -> {{ cookiecutter.app_name }}:
    return detail_model(actor, {{ cookiecutter.app_name }}Permissions.READ, {{ cookiecutter.app_slug }})


def delete_{{ cookiecutter.app_slug_plural }}(data: DeleteRequest, actor: User):
    delete_models(actor, {{ cookiecutter.app_name }}Permissions.DELETE, data)
