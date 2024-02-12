import pytest

from supply_points.services import (
    supply_point_create,
    supply_point_update,
)


@pytest.mark.django_db
def test_create_supply_point_channel_admin(channel_admin, supply_point_create_request):
    new_supply_point = supply_point_create(supply_point_create_request, channel_admin)
    assert new_supply_point.alias == supply_point_create_request.alias


@pytest.mark.django_db
def test_update_supply_point_channel_admin(
    channel_admin, supply_point, supply_point_update_request
):
    updatable_supply_point = supply_point_update(
        supply_point, supply_point_update_request, channel_admin
    )
    assert updatable_supply_point.alias == supply_point_update_request.alias
