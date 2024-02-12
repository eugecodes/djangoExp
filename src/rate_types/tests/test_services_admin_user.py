import pytest

from rate_types.services import (
    rate_type_create,
    rate_type_update,
)


@pytest.mark.django_db
def test_create_rate_type_admin_user(admin_user, rate_type_create_request):
    new_rate_type = rate_type_create(rate_type_create_request, admin_user)
    assert new_rate_type.name == rate_type_create_request.name


@pytest.mark.django_db
def test_update_rate_type_admin_user(admin_user, rate_type, rate_type_update_request):
    updatable_rate_type = rate_type_update(
        rate_type, rate_type_update_request, admin_user
    )
    assert updatable_rate_type.name == rate_type_update_request.name
