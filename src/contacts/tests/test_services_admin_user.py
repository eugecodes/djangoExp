import pytest

from contacts.services import (
    contact_create,
    contact_update,
)


@pytest.mark.django_db
def test_create_contact_admin_user(admin_user, contact_create_request):
    new_contact = contact_create(contact_create_request, admin_user)
    assert new_contact.name == contact_create_request.name


@pytest.mark.django_db
def test_update_contact_admin_user(admin_user, contact, contact_update_request):
    updatable_contact = contact_update(contact, contact_update_request, admin_user)
    assert updatable_contact.name == contact_update_request.name
