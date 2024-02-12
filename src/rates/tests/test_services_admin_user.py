import pytest

from rates.services import (
    rate_create,
    rate_update,
)


@pytest.mark.django_db
def test_create_rate_admin_user(admin_user, rate_create_request):
    new_rate = rate_create(rate_create_request, admin_user)
    assert new_rate.name == rate_create_request.name


@pytest.mark.django_db
def test_update_rate_admin_user(admin_user, rate, rate_update_request):
    updatable_rate = rate_update(rate, rate_update_request, admin_user)
    assert updatable_rate.name == rate_update_request.name
