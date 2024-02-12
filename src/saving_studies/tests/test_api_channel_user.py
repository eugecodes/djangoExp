import pytest
from guardian.shortcuts import assign_perm

from common.client import client
from common.pagination import EMPTY_LIST_RESPONSE
from saving_studies.models import SavingStudy
from saving_studies.permissions import SavingStudyPermissions

API_URL = f"/studies/"


@pytest.mark.django_db
def test_get_list(channel_user, saving_study):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_get_list_no_permission(channel_user, saving_study):
    client.set_user(channel_user)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == EMPTY_LIST_RESPONSE


@pytest.mark.django_db
def test_get_list(channel_user, saving_study):
    client.set_user(channel_user)
    assign_perm(SavingStudyPermissions.READ, channel_user, saving_study)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_saving_study_not_allowed(channel_user, saving_study_create_request):
    client.set_user(channel_user)
    response = client.post(API_URL, json=saving_study_create_request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_saving_study_allowed(channel_user, saving_study_create_request):
    client.set_user(channel_user)
    assign_perm(SavingStudyPermissions.CREATE, channel_user)
    response = client.post(API_URL, json=saving_study_create_request)
    new_saving_study = SavingStudy.objects.last()
    assert response.status_code == 201
    json_response = response.json()
    assert json_response["id"] == new_saving_study.id
    assert json_response["cups"] == saving_study_create_request.cups


@pytest.mark.django_db
def test_update_saving_study_not_allowed(
    channel_user, saving_study, saving_study_update_request
):
    client.set_user(channel_user)
    response = client.put(
        f"{API_URL}{saving_study.id}", json=saving_study_update_request
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_saving_study_allowed(
    channel_user, saving_study, saving_study_update_request
):
    client.set_user(channel_user)
    assign_perm(SavingStudyPermissions.EDIT, channel_user, saving_study)
    response = client.put(
        f"{API_URL}{saving_study.id}", json=saving_study_update_request
    )
    assert response.status_code == 200
    saving_study.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == saving_study.id


@pytest.mark.django_db
def test_partial_update_saving_study_not_allowed(
    channel_user, saving_study, saving_study_update_request
):
    client.set_user(channel_user)
    response = client.patch(
        f"{API_URL}{saving_study.id}", json=saving_study_update_request
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_partial_update_saving_study_allowed(
    channel_user, saving_study, saving_study_update_request
):
    client.set_user(channel_user)
    assign_perm(SavingStudyPermissions.EDIT, channel_user, saving_study)
    response = client.patch(
        f"{API_URL}{saving_study.id}", json=saving_study_update_request
    )
    assert response.status_code == 200
    saving_study.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == saving_study.id
