import pytest
from guardian.shortcuts import assign_perm
from ninja.errors import AuthenticationError

from energy_costs.permissions import EnergyCostPermissions
from energy_costs.services import (
    energy_cost_create,
    energy_cost_update,
)


@pytest.mark.django_db
def test_create_energy_cost_channel_user_not_allowed(
    channel_user, energy_cost_create_request
):
    with pytest.raises(AuthenticationError):
        energy_cost_create(energy_cost_create_request, channel_user)


@pytest.mark.django_db
def test_create_energy_cost_channel_user_allowed(
    channel_user, energy_cost_create_request
):
    assign_perm(EnergyCostPermissions.CREATE, channel_user)
    new_energy_cost = energy_cost_create(energy_cost_create_request, channel_user)
    assert new_energy_cost.code == energy_cost_create_request.code


@pytest.mark.django_db
def test_update_energy_cost_channel_user_not_allowed(
    channel_user, energy_cost, energy_cost_update_request
):
    with pytest.raises(AuthenticationError):
        energy_cost_update(energy_cost, energy_cost_update_request, channel_user)


@pytest.mark.django_db
def test_update_energy_cost_channel_user_allowed(
    channel_user, energy_cost, energy_cost_update_request
):
    assign_perm(EnergyCostPermissions.EDIT, channel_user, energy_cost)
    updatable_energy_cost = energy_cost_update(
        energy_cost, energy_cost_update_request, channel_user
    )
    assert updatable_energy_cost.code == energy_cost_update_request.code
