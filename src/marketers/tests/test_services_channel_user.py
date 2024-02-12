import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from marketers.permissions import MarketerPermissions
from marketers.services import (
    marketer_create,
    marketer_update,
)


@pytest.mark.django_db
def test_create_marketer_channel_user_not_allowed(
    channel_user, marketer_create_request
):
    with pytest.raises(AuthenticationError):
        marketer_create(marketer_create_request, channel_user)


@pytest.mark.django_db
def test_create_marketer_channel_user_allowed(channel_user, marketer_create_request):
    assign_perm(MarketerPermissions.CREATE, channel_user)
    new_marketer = marketer_create(marketer_create_request, channel_user)
    assert new_marketer.name == marketer_create_request.name


@pytest.mark.django_db
def test_update_marketer_channel_user_not_allowed(
    channel_user, marketer, marketer_update_request
):
    with pytest.raises(AuthenticationError):
        marketer_update(marketer, marketer_update_request, channel_user)


@pytest.mark.django_db
def test_update_marketer_channel_user_allowed(
    channel_user, marketer, marketer_update_request
):
    assign_perm(MarketerPermissions.EDIT, channel_user, marketer)
    updatable_marketer = marketer_update(
        marketer, marketer_update_request, channel_user
    )
    assert updatable_marketer.name == marketer_update_request.name
