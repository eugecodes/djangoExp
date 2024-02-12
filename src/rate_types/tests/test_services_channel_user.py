import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from rate_types.permissions import RateTypePermissions
from rate_types.services import (
    rate_type_create,
    rate_type_update,
)


@pytest.mark.django_db
def test_create_rate_type_channel_user_not_allowed(
    channel_user, rate_type_create_request
):
    with pytest.raises(AuthenticationError):
        rate_type_create(rate_type_create_request, channel_user)


@pytest.mark.django_db
def test_create_rate_type_channel_user_allowed(channel_user, rate_type_create_request):
    assign_perm(RateTypePermissions.CREATE, channel_user)
    new_rate_type = rate_type_create(rate_type_create_request, channel_user)
    assert new_rate_type.name == rate_type_create_request.name


@pytest.mark.django_db
def test_update_rate_type_channel_user_not_allowed(
    channel_user, rate_type, rate_type_update_request
):
    with pytest.raises(AuthenticationError):
        rate_type_update(rate_type, rate_type_update_request, channel_user)


@pytest.mark.django_db
def test_update_rate_type_channel_user_allowed(
    channel_user, rate_type, rate_type_update_request
):
    assign_perm(RateTypePermissions.EDIT, channel_user, rate_type)
    updatable_rate_type = rate_type_update(
        rate_type, rate_type_update_request, channel_user
    )
    assert updatable_rate_type.name == rate_type_update_request.name
