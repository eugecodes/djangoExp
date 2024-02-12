import pytest

from clients.services import (
    client_create,
    client_update,
)


@pytest.mark.django_db
def test_create_client_admin_user(admin_user, client_create_request):
    new_client = client_create(client_create_request, admin_user)
    assert new_client.alias == client_create_request.alias
    assert new_client.fiscal_name == client_create_request.fiscal_name
    assert new_client.cif == client_create_request.cif


@pytest.mark.django_db
def test_update_client_admin_user(admin_user, channel_client, client_update_request):
    updatable_client = client_update(channel_client, client_update_request, admin_user)
    assert updatable_client.alias == client_update_request.alias
    assert updatable_client.fiscal_name == client_update_request.fiscal_name
    assert updatable_client.cif == client_update_request.cif
