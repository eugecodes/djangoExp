import pytest

from saving_studies.services.base import (
    saving_study_create,
    saving_study_update,
)


@pytest.mark.django_db
def test_create_saving_study_channel_admin(channel_admin, saving_study_create_request):
    new_saving_study = saving_study_create(saving_study_create_request, channel_admin)
    assert new_saving_study.cups == saving_study_create_request.cups


@pytest.mark.django_db
def test_update_saving_study_channel_admin(
    channel_admin, saving_study, saving_study_update_request
):
    updatable_saving_study = saving_study_update(
        saving_study, saving_study_update_request, channel_admin
    )
    assert updatable_saving_study.client_type == saving_study_update_request.client_type
