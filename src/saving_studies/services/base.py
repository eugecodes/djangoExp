from auditlog.context import set_actor
from django.contrib.auth import get_user_model
from guardian.shortcuts import get_objects_for_user
from ninja import FilterSchema
from ninja.errors import AuthenticationError, ValidationError

from common.api.requests import DeleteRequest
from common.services import model_update, delete_models, detail_model
from saving_studies.api.schemas.requests import (
    SavingStudyRequest,
    SavingStudyUpdateRequest,
)
from saving_studies.models import SavingStudy
from saving_studies.permissions import SavingStudyPermissions

User = get_user_model()


def saving_study_list(filters: FilterSchema, actor: User):
    if actor.is_superuser:
        saving_studies = SavingStudy.objects.all()
    else:
        saving_studies = get_objects_for_user(actor, SavingStudyPermissions.READ)
    saving_studies = filters.filter(saving_studies)
    return saving_studies


def saving_study_create(data: SavingStudyRequest, actor: User):
    if not actor.has_perm(SavingStudyPermissions.CREATE) and not actor.is_superuser:
        raise AuthenticationError
    if data.channel_id is None:
        raise ValidationError(errors=[{"channel_id": "required"}])
    with set_actor(actor):
        saving_study = SavingStudy.objects.create(**data.dict())
    return saving_study


def saving_study_update(
    saving_study: SavingStudy, data: SavingStudyUpdateRequest, actor: User
) -> SavingStudy:
    if (
        not actor.has_perm(SavingStudyPermissions.EDIT, saving_study)
        and not actor.is_superuser
    ):
        raise AuthenticationError
    return model_update(saving_study, data, actor)


def saving_study_detail(saving_study: SavingStudy, actor: User) -> SavingStudy:
    return detail_model(actor, SavingStudyPermissions.READ, saving_study)


def delete_saving_studies(data: DeleteRequest, actor: User):
    delete_models(actor, SavingStudyPermissions.DELETE, data)
