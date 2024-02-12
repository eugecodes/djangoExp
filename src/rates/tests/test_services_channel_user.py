import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from rates.permissions import RatePermissions
from rates.services import (
    rate_create,
    rate_update,
)


@pytest.mark.django_db
def test_create_rate_channel_user_not_allowed(channel_user, rate_create_request):
    with pytest.raises(AuthenticationError):
        rate_create(rate_create_request, channel_user)


@pytest.mark.django_db
def test_create_rate_channel_user_allowed(channel_user, rate_create_request):
    assign_perm(RatePermissions.CREATE, channel_user)
    new_rate = rate_create(rate_create_request, channel_user)
    assert new_rate.name == rate_create_request.name


@pytest.mark.django_db
def test_update_rate_channel_user_not_allowed(channel_user, rate, rate_update_request):
    with pytest.raises(AuthenticationError):
        rate_update(rate, rate_update_request, channel_user)


@pytest.mark.django_db
def test_update_rate_channel_user_allowed(channel_user, rate, rate_update_request):
    assign_perm(RatePermissions.EDIT, channel_user, rate)
    updatable_rate = rate_update(rate, rate_update_request, channel_user)
    assert updatable_rate.name == rate_update_request.name
