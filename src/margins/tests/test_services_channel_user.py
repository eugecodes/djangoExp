import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from margins.permissions import MarginPermissions
from margins.services import (
    margin_create,
    margin_update,
)


@pytest.mark.django_db
def test_create_margin_channel_user_not_allowed(channel_user, margin_create_request):
    with pytest.raises(AuthenticationError):
        margin_create(margin_create_request, channel_user)


@pytest.mark.django_db
def test_create_margin_channel_user_allowed(channel_user, margin_create_request):
    assign_perm(MarginPermissions.CREATE, channel_user)
    new_margin = margin_create(margin_create_request, channel_user)
    assert new_margin.type == margin_create_request.type


@pytest.mark.django_db
def test_update_margin_channel_user_not_allowed(
    channel_user, margin, margin_update_request
):
    with pytest.raises(AuthenticationError):
        margin_update(margin, margin_update_request, channel_user)


@pytest.mark.django_db
def test_update_margin_channel_user_allowed(
    channel_user, margin, margin_update_request
):
    assign_perm(MarginPermissions.EDIT, channel_user, margin)
    updatable_margin = margin_update(margin, margin_update_request, channel_user)
    assert updatable_margin.type == margin_update_request.type
