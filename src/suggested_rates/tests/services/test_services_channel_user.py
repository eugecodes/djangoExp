import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from suggested_rates.permissions import SuggestedRatePermissions
from suggested_rates.services.base import (
    suggested_rate_create,
    suggested_rate_update,
)


@pytest.mark.django_db
def test_create_suggested_rate_channel_user_not_allowed(
    channel_user, suggested_rate_create_request
):
    with pytest.raises(AuthenticationError):
        suggested_rate_create(suggested_rate_create_request, channel_user)


@pytest.mark.django_db
def test_create_suggested_rate_channel_user_allowed(
    channel_user, suggested_rate_create_request
):
    assign_perm(SuggestedRatePermissions.CREATE, channel_user)
    new_suggested_rate = suggested_rate_create(
        suggested_rate_create_request, channel_user
    )
    assert new_suggested_rate.name == suggested_rate_create_request.name


@pytest.mark.django_db
def test_update_suggested_rate_channel_user_not_allowed(
    channel_user, suggested_rate, suggested_rate_update_request
):
    with pytest.raises(AuthenticationError):
        suggested_rate_update(
            suggested_rate, suggested_rate_update_request, channel_user
        )


@pytest.mark.django_db
def test_update_suggested_rate_channel_user_allowed(
    channel_user, suggested_rate, suggested_rate_update_request
):
    assign_perm(SuggestedRatePermissions.EDIT, channel_user, suggested_rate)
    updatable_suggested_rate = suggested_rate_update(
        suggested_rate, suggested_rate_update_request, channel_user
    )
    assert updatable_suggested_rate.name == suggested_rate_update_request.name
