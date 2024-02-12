import pytest

from contacts.services import (
    contact_create,
    contact_update,
)


@pytest.mark.django_db
def test_create_contact_channel_admin(channel_admin, contact_create_request):
    new_contact = contact_create(contact_create_request, channel_admin)
    assert new_contact.name == contact_create_request.name


@pytest.mark.django_db
def test_update_contact_channel_admin(channel_admin, contact, contact_update_request):
    updatable_contact = contact_update(contact, contact_update_request, channel_admin)
    assert updatable_contact.name == contact_update_request.name
