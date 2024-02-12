import pytest

from suggested_rates.services.base import (
    suggested_rate_create,
    suggested_rate_update,
)


@pytest.mark.django_db
def test_create_suggested_rate_channel_admin(
    channel_admin, suggested_rate_create_request
):
    new_suggested_rate = suggested_rate_create(
        suggested_rate_create_request, channel_admin
    )
    assert new_suggested_rate.name == suggested_rate_create_request.name


@pytest.mark.django_db
def test_update_suggested_rate_channel_admin(
    channel_admin, suggested_rate, suggested_rate_update_request
):
    updatable_suggested_rate = suggested_rate_update(
        suggested_rate, suggested_rate_update_request, channel_admin
    )
    assert updatable_suggested_rate.name == suggested_rate_update_request.name
