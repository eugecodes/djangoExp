import pytest

from suggested_rates.services.base import (
    suggested_rate_create,
    suggested_rate_update,
)


@pytest.mark.django_db
def test_create_suggested_rate_admin_user(admin_user, suggested_rate_create_request):
    new_suggested_rate = suggested_rate_create(
        suggested_rate_create_request, admin_user
    )
    assert new_suggested_rate.name == suggested_rate_create_request.name


@pytest.mark.django_db
def test_update_suggested_rate_admin_user(
    admin_user, suggested_rate, suggested_rate_update_request
):
    updatable_suggested_rate = suggested_rate_update(
        suggested_rate, suggested_rate_update_request, admin_user
    )
    assert updatable_suggested_rate.name == suggested_rate_update_request.name
