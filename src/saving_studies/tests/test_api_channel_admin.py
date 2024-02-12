import pytest

from common.client import client
from saving_studies.models import SavingStudy

API_URL = f"/studies/"


@pytest.mark.django_db
def test_get_list(channel_admin, saving_study):
    client.set_user(channel_admin)
    response = client.get(API_URL)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["total"] == 1
    assert json_response["page"] == 1
    assert json_response["size"] == 10


@pytest.mark.django_db
def test_create_saving_study(channel_admin, saving_study_create_request):
    client.set_user(channel_admin)
    response = client.post(API_URL, json=saving_study_create_request)
    new_saving_study = SavingStudy.objects.last()
    json_response = response.json()
    assert json_response["id"] == new_saving_study.id
    assert json_response["cups"] == saving_study_create_request.cups


@pytest.mark.django_db
def test_update_saving_study(channel_admin, saving_study, saving_study_update_request):
    client.set_user(channel_admin)
    response = client.put(
        f"{API_URL}{saving_study.id}", json=saving_study_update_request
    )
    saving_study.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == saving_study.id


@pytest.mark.django_db
def test_partial_update_saving_study(
    channel_admin, saving_study, saving_study_update_request
):
    client.set_user(channel_admin)
    response = client.patch(
        f"{API_URL}{saving_study.id}", json=saving_study_update_request
    )
    saving_study.refresh_from_db()
    json_response = response.json()
    assert json_response["id"] == saving_study.id
