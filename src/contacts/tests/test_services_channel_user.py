import pytest
from ninja.errors import AuthenticationError
from guardian.shortcuts import assign_perm
from contacts.permissions import ContactPermissions
from contacts.services import (
    contact_create,
    contact_update,
)


@pytest.mark.django_db
def test_create_contact_channel_user_not_allowed(channel_user, contact_create_request):
    with pytest.raises(AuthenticationError):
        contact_create(contact_create_request, channel_user)

@pytest.mark.django_db
def test_create_contact_channel_user_allowed(channel_user, contact_create_request):
    assign_perm(ContactPermissions.CREATE, channel_user)
    new_contact = contact_create(contact_create_request, channel_user)
    assert new_contact.name == contact_create_request.name


@pytest.mark.django_db
def test_update_contact_channel_user_not_allowed(channel_user, contact, contact_update_request):
    with pytest.raises(AuthenticationError):
        contact_update(contact, contact_update_request, channel_user)


@pytest.mark.django_db
def test_update_contact_channel_user_allowed(channel_user, contact, contact_update_request):
    assign_perm(ContactPermissions.EDIT, channel_user, contact)
    updatable_contact = contact_update(contact, contact_update_request, channel_user)
    assert updatable_contact.name == contact_update_request.name