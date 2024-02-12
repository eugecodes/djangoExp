import pytest

from supply_points.services import (
    supply_point_create,
    supply_point_update,
)


@pytest.mark.django_db
def test_create_supply_point_admin_user(admin_user, supply_point_create_request):
    new_supply_point = supply_point_create(supply_point_create_request, admin_user)
    assert new_supply_point.alias == supply_point_create_request.alias


@pytest.mark.django_db
def test_update_supply_point_admin_user(
    admin_user, supply_point, supply_point_update_request
):
    updatable_supply_point = supply_point_update(
        supply_point, supply_point_update_request, admin_user
    )
    assert updatable_supply_point.alias == supply_point_update_request.alias
