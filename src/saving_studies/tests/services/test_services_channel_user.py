import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from saving_studies.permissions import SavingStudyPermissions
from saving_studies.services.base import (
    saving_study_create,
    saving_study_update,
)


@pytest.mark.django_db
def test_create_saving_study_channel_user_not_allowed(
    channel_user, saving_study_create_request
):
    with pytest.raises(AuthenticationError):
        saving_study_create(saving_study_create_request, channel_user)


@pytest.mark.django_db
def test_create_saving_study_channel_user_allowed(
    channel_user, saving_study_create_request
):
    assign_perm(SavingStudyPermissions.CREATE, channel_user)
    new_saving_study = saving_study_create(saving_study_create_request, channel_user)
    assert new_saving_study.cups == saving_study_create_request.cups


@pytest.mark.django_db
def test_update_saving_study_channel_user_not_allowed(
    channel_user, saving_study, saving_study_update_request
):
    with pytest.raises(AuthenticationError):
        saving_study_update(saving_study, saving_study_update_request, channel_user)


@pytest.mark.django_db
def test_update_saving_study_channel_user_allowed(
    channel_user, saving_study, saving_study_update_request
):
    assign_perm(SavingStudyPermissions.EDIT, channel_user, saving_study)
    updatable_saving_study = saving_study_update(
        saving_study, saving_study_update_request, channel_user
    )
    assert updatable_saving_study.client_type == saving_study_update_request.client_type
