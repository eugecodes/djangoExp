import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from supply_points.permissions import SupplyPointPermissions
from supply_points.services import (
    supply_point_create,
    supply_point_update,
)


@pytest.mark.django_db
def test_create_supply_point_channel_user_not_allowed(
    channel_user, supply_point_create_request
):
    with pytest.raises(AuthenticationError):
        supply_point_create(supply_point_create_request, channel_user)


@pytest.mark.django_db
def test_create_supply_point_channel_user_allowed(
    channel_user, supply_point_create_request
):
    assign_perm(SupplyPointPermissions.CREATE, channel_user)
    new_supply_point = supply_point_create(supply_point_create_request, channel_user)
    assert new_supply_point.alias == supply_point_create_request.alias


@pytest.mark.django_db
def test_update_supply_point_channel_user_not_allowed(
    channel_user, supply_point, supply_point_update_request
):
    with pytest.raises(AuthenticationError):
        supply_point_update(supply_point, supply_point_update_request, channel_user)


@pytest.mark.django_db
def test_update_supply_point_channel_user_allowed(
    channel_user, supply_point, supply_point_update_request
):
    assign_perm(SupplyPointPermissions.EDIT, channel_user, supply_point)
    updatable_supply_point = supply_point_update(
        supply_point, supply_point_update_request, channel_user
    )
    assert updatable_supply_point.alias == supply_point_update_request.alias
